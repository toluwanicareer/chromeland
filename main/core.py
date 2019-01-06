import requests
from bs4 import BeautifulSoup
import pdb
#from docx import Document
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def dms(tracking_id):
    data = {
        'txtCargoContainer': tracking_id,
        'txtSource': 'Simple',
        'cboLang': 'E',
        'cmdShow': 'Rechercher / Search'
    }
    link='http://tracking.entrepotdms.com/Detail.asp'
    response=requests.post(link, data=data)
    soup=BeautifulSoup(response.content, 'html.parser')
    destuff_date=soup.find('td', text='Destuff Date').find_next_sibling('td').text.strip()
    storage_date = soup.find('td', text='Storage Date').find_next_sibling('td').text.strip()
    df=soup.find('font', {'color':'AF0000'}).text.strip().split(':')[1]
    delivery_date= ''.join(e for e in df[1:])
    dock_fee_guarantee=soup.find('td', text='Dock Fee : Guaranteed').find_next('tr').find_all('td')[5].text.strip()
    dock_fee=soup.find('td', text='Dock Fee').find_next('tr').find_all('td')[5].text.strip()
    return {'Destuff Date':destuff_date,
            'Storage Date':storage_date,
            'Delivery Date':delivery_date,
            'dock_fee_guarantee':dock_fee_guarantee,
            'dock_fee':dock_fee}


def Shulterm(tracking_id):
    link='http://newextranet.shulterm.com/Default.aspx'
    data={
        'Find':'81351053667'#tracking_id
    }
    response=requests.post(link, data=data)
    soup=BeautifulSoup(response.content, 'html.parser')
    received_on=soup.find('td', text='Received On').find_next('td').text.strip()
    unloaded_date=soup.find('td', text='Unloaded On').find_next('td').text.strip()
    storage_start_on=soup.find('td', text='Storage Starts On').find_next('td').text.strip()
    custom_clearance_issued_on=soup.find('td', text='Customs Clearance Issued On').find_next('td').text.strip()
    cancelled_manifest=soup.find('td', text='Cancelled Manifest 1/1 Received On').find_next('td').text.strip()
    release_order=soup.find('td', text='Release Order 1/1 Received On').find_next('td').text.strip()
    delivery_date=soup.find('table', class_='ShipmentListTable').find_all('td')[14].text.strip()
    appointment=soup.find('table', class_='ShipmentListTable').find_all('td')[12].text.strip()
    transport = soup.find('table', class_='ShipmentListTable').find_all('td')[13].text.strip()
    return {
        'Received On':received_on,
        'unloaded_date':unloaded_date,
        'Storage Start On':storage_start_on,
        'customs_date':custom_clearance_issued_on,
        'Cancelled Manifest 1/1 Received On':cancelled_manifest,
        'Release Order 1/1 Received On':release_order,
        'delivery_date':delivery_date,
        'Appointment':appointment,
        'Transport': transport
    }

def lafrance(tracking_id):
    link='https://www.lafrance.qc.ca/lcms/view/external/cargo/status.do?conversationPropagation=nested&returnTo=&ccn='+tracking_id+'&cid=261697'
    response=requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    tds=soup.find('td', class_='layout-column-left-50').table.find_all('td', class_='label-container')
    result=dict()
    for td in tds :
        text=td.text.strip()
        check_list=['Arrival Date', 'Storage Date', 'Delivery Status', 'Delivery Appointment', 'Shipped Time', 'Delivery Time']
        if text in check_list:
            key=check_list[check_list.index(text)]
            value=td.find_next_sibling('td', class_='edition-container').text.strip()
            result[key]=value
    return result

def airpro(tracking_id):
    link='http://www.airprotransport.com/neo/index.php/track/view'
    data={'cargoctrl':tracking_id,
          'mawb':''
          }
    response=requests.post(link, data=data)
    soup=BeautifulSoup(response.content, 'html.parser')
    #doc=Document()
    ##doc.add_paragraph(response.text)
    #doc.save('source.docx')
    #TODO waiting for field
    div=soup.find('div', class_='form-group')
    div=div.find_next_sibling('div', class_='form-group')
    labels=div.find_all('label')
    response=dict()
    result=[response.update({label.text.strip(): label.find_next_sibling('input')['value']}) for label in labels]
    #pdb.set_trace()
    div = div.find_next_sibling('div', class_='form-group')
    labels = div.find_all('label')
    result = [response.update({label.text.strip(): label.find_next_sibling('input')['value']}) for label in labels]
    return response


def cp():
    link='https://ecprod.cn.ca/quick_login_en.html'
    driver = webdriver.Chrome(executable_path='C:\\Users\\dell\\PycharmProjects\\shipping_api\\driver\\chromedriver_win32\\chromedriver.exe')
    driver.get(link)
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    username.clear()
    password.clear()
    username.send_keys("neilsabharwal")
    password.send_keys("qwert1111")
    btn=driver.find_element_by_class_name('image')
    btn.click()
    driver.get('https://ecprod.cn.ca/velocity/IMShipmentStatus/english/CFF_ImdShipmentStatus')
    final_input=driver.find_element_by_id("cars")
    final_input.clear()
    final_input.send_keys('FSCU999098')
    submit_btn=driver.find_element_by_id('submit')
    submit_btn.click()


def canchi(tracking_id):
    link='http://fxoffice.canchi.com/Tracking/Login.asp'
    data={'DocNo':tracking_id,
          'Submit':'Track',
          'Name':'',
          'Password':'',
    }
    response=requests.post(link, data=data)
    soup=BeautifulSoup(response.content, 'html.parser')
    arrival_date=soup.find('b', text='Arrival Date').find_next('b').text.strip()
    unloaded_date=soup.find('b', text='Unloading Date').find_next('b').text.strip()
    storage_date=soup.find('b', text='Storage Date').find_next('b').text.strip()
    custom_release=soup.find('b', text='Customs Release').find_next('b').text.strip()
    status=soup.find_all('b')[23].find_next('b').text.strip().replace('\t', '').replace('\n','').replace('\r', '')
    return {
        'Arrival Date':arrival_date,
        'unloaded_date':unloaded_date,
        'Storage Date':storage_date,
        'Custom Release':custom_release,
        'Moved / Status':status,
    }












