from selenium import webdriver
from lxml import etree
import time
import json
from selenium.webdriver.chrome.options import Options

# 设置无头chrome driver
chrome_options = Options()
chrome_options.add_argument("--headless")

def main(name):
    # 请求网页
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.lagou.com/jobs/list_{}/p-city_0?px=default#filterBox'.format(name))
    driver.maximize_window()
    page = 0
    t = time.strftime('%Y-%m-%d   ', time.localtime())

    while True:
        # 获取信息
        page += 1
        html = driver.page_source
        html = etree.HTML(html)
        li_list = html.xpath('//div[@class="s_position_list "]/ul/li')
        print('正在爬取第{}页'.format(page))
        content_list = []
        for li in li_list:
            content = {}
            content['job_name'] = ''.join(li.xpath('.//div[@class="p_top"]/a[@class="position_link"]/h3/text()'))
            content['company_position'] = ''.join(li.xpath('.//div[@class="p_top"]/a[@class="position_link"]//em/text()'))
            content['pubilish_time'] = t + ''.join(li.xpath('.//div[@class="p_top"]/span[@class="format-time"]/text()'))
            content['company_name'] = ''.join(li.xpath('./@data-company'))
            content['salary'] = ''.join(li.xpath('./@data-salary'))
            content['requests'] = ''.join(li.xpath('.//div[@class="p_bot"]/div[@class="li_b_l"]/text()')).strip()
            content['industry'] = ''.join(li.xpath('.//div[@class="company"]//div[@class="industry"]/text()')).strip()
            for span in li.xpath('.//div[@class="li_b_l"]/span'):
                content['jobs_Lable'] = span.xpath('./text()') if li.xpath('.//div[@class="li_b_l"]/span').index(
                    span) == 0 else content['jobs_Lable'] + span.xpath('./text()')
            content['jobs_Lable'] = ' / '.join(content['jobs_Lable']).strip()
            content['benefit'] = ''.join(li.xpath('.//div[@class="li_b_r"]/text()'))
            content['Logo'] = 'https:' + ''.join(li.xpath('.//div[@class="com_logo"]//img/@src'))
            content_list.append(content)
        file_path = '{}.txt'.format(name)
        # 保存这一页数据
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(content_list, ensure_ascii=False, indent=2))

        # 判断是否还有下一页
        if ''.join(html.xpath('//span[@action="next"]/@class')) == 'pager_next ':
            while True:
                try:
                    driver.find_element_by_class_name('pager_next').click()
                    break
                except:
                    print('广告弹窗已关闭')
                    driver.find_element_by_class_name('body-btn').click()
                    time.sleep(1)
        else:
            break
        # 给页面反应时间
        time.sleep(2)

    # 退出浏览器
    print('数据爬取完毕')
    driver.quit()

if __name__ == '__main__':
    name = input('请输入想要爬取相关工作的名称：')
    main(name)