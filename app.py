import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import time
import re
import io

st.set_page_config(page_title="RUZ Planner", layout="wide")
st.title("📅 Расписание")

GROUP_MAP = {

  "в3733801/20101": "44410",
  "3730105/30101": "44217",
  "3733801/30101": "44178",
  "в3733801/30101": "44400",
  "в3733801/30130": "44401",
  "в3733801/30131": "44402",
  "3733801/30401": "44186",
  "3733801/30501": "44179",
  "3733801/30981": "44183",
  "3733801/30982": "44184",
  "3733801/31401": "44182",
  "3733801/31801": "44185",
  "3733801/32901": "44180",
  "3733801/33001": "44181",
  "3730105/40101": "44115",
  "3733801/40101": "44076",
  "в3733801/40130": "44386",
  "в3733801/40131": "44387",
  "3733801/40401": "44078",
  "в3733801/40401": "44388",
  "3733801/40501": "44073",
  "3733801/40981": "44081",
  "3733801/40982": "44080",
  "3733801/41401": "44077",
  "3733801/41801": "44079",
  "3733801/42901": "44074",
  "в3743801/41401": "44392",
  "в3733801/50130": "45738",
  "3740105/50101": "44021",
  "3740105/50201": "44022",
  "3740105/50301": "44023",
  "3742707/50101": "44015",
  "3742707/50201": "44016",
  "3742707/50301": "44017",
  "3743801/50401": "43976",
  "3743801/51401": "43975",
  "3743801/52701": "43977",
  "3743801/52801": "43980",
  "3743801/53001": "43978",
  "3743801/53101": "43979",
  "в3730105/60001": "44382",
  "3733801/60001": "43864",
  "3733801/60002": "43865",
  "3733801/60003": "43866",
  "3733801/60004": "43867",
  "3733801/60005": "43868",
  "3733801/60006": "43869",
  "3733801/60981": "43870",
  "3733801/62901": "43871",
  "3740105/60101": "43932",
  "3740105/60201": "43933",
  "3740105/60301": "43934",
  "3742707/60101": "43927",
  "3742707/60301": "43928",
  "3743801/60401": "43889",
  "3743801/61401": "43893",
  "3743801/62701": "43890",
  "3743801/63001": "43891",
  "3743801/63101": "43892",
  "3730105/50001": "44019",
  "3730105/50002": "44020",
  "3733801/50001": "43951",
  "3733801/50002": "43952",
  "3733801/50003": "43953",
  "3733801/50004": "43954",
  "3733801/50005": "43955",
  "3733801/50006": "43956",
  "3733801/50981": "43957",
  "3733801/52901": "43958",
  "3734301/50001": "44002",
  "3734302/50001": "44011",
  "3734302/50381": "44012",
  "3734303/50001": "44013",
  "3734303/50002": "44014",
  "3733801/43001": "44075",
  "в3730105/50001": "44385",
  "в3733801/50001": "44383",
  "3730105/60001": "43930",
  "3730105/60002": "43931",
  "3730105/60003": "44223",
  "3753801/20101": "44220",
"3753801/20102": "44219",
"3753801/20401": "44218",
"3753801/30101": "44211",
"3753801/30102": "44212",
"3753801/30103": "44213",
"3753801/40101": "44109",
"3753801/40102": "44108",
"3753801/40401": "44110",
"3753801/50001": "44008",
"3753801/50002": "44009",
"3753801/50003": "44010",
"3753801/60001": "43922",
"3753801/60002": "43923",
  "3733801/40102":"44072",
  "в3733801/60001":"44381"
#"з3753801/10101": "Загрузить позже",
#"з3753801/20101": "Загрузить позже",
#"з3753801/20130": "Загрузить позже",
#"з3753801/30101": "Загрузить позже",
#"з3753801/30102": "Загрузить позже",
#"з3753801/30103": "Загрузить позже",
#"з3753801/40101": "Загрузить позже",
#"з3753801/40102": "Загрузить позже",
#"з3753801/40130": "Загрузить позже",
#"з3753801/50001": "Загрузить позже",
#"з3753801/60001": "Загрузить позже",
# "з3743809/40101": "Не найдено",
# "з3743801/40401": "Не найдено",
# "з3743801/41401": "Не найдено",
# "з3743801/42001": "Не найдено",
# "в3733801/50101": "Не найдено",
# "з3743801/52001": "Не найдено",
# "3733801/60982": "Не найдено",
# "3733801/63201": "Не найдено",
# "з3743801/62001": "Не найдено",
# "3743801/62801": "Не найдено",
# "з3743801/63101": "Не найдено",
# "3733801/50982": "Не найдено",
# "3730105/40001": "Не найдено",
# "3733801/40001": "Не найдено",
# "3733801/40002": "Не найдено",
# "3733801/40003": "Не найдено",
# "3733801/40004": "Не найдено",
# "3733801/40005": "Не найдено",
# "3733801/40006": "Не найдено",
# "3733801/40007": "Не найдено",
# "в3733801/50002": "Не найдено",
# "в3733801/40001": "Не найдено",
# "в3733801/30001": "Не найдено",
# "в3733801/30430": "Не найдено",
# "в3733801/30431": "Не найдено"
}

TEACHER_MAP = {
    
    "Абакарова Рабият Шамсулвараевна": "26987",
    "Абдуллаев Арсен Теймурович": "25954",
    "Абрамчикова Наталья Викторовна": "20719",
    "Анзина София Дмитриевна": "998369",
    "Антышева Елена Робертовна": "99892",
    "Артеева Валерия Семеновна": "20150",
    "Бабкин Александр Васильевич": "698",
    "Бабкин Иван Александрович": "16851",
    "Батаев Алексей Владимирович": "480",
    "Безручко Денис Сергеевич": "21118",
    "Благой Никита Арсенович": "24879",
    "Богданова Татьяна Александровна": "652",
    "Боровкова Валерия Анатольевна": "99809",
    "Бразовская Виктория Владимировна": "21810",
    "Бугаева Татьяна Михайловна": "4619",
    "Бурова Екатерина Валерьевна": "98786",
    "Веревка Татьяна Владимировна": "16791",
    "Веселов Андрей Викторович": "26946",
    "Викторова Наталья Геннадьевна": "99766",
    "Гончарова Наталья Леонидовна": "12525",
    "Гузикова Людмила Александровна": "1606",
    "Гутман Светлана Семеновна": "1651",
    "Дементьева Анастасия Александровна": "26911",
    "Дмитриев Николай Дмитриевич": "21633",
    "Долотова Наталья Леонидовна": "1810",
    "Дуболазова Юлия Андреевна": "15884",
    "Евсеева Ксения Владимировна": "20041",
    "Еремина Ирина Александровна": "23188",
    "Зайцев Андрей Александрович": "19997",
    "Ковалевская Валерия Валерьевна": "25248",
    "Конников Евгений Александрович": "12534",
    "Королёва Екатерина Васильевна": "9591",
    "Кочинев Юрий Юрьевич": "3240",
    "Кранина Анна Дмитриевна": "16553",
    "Краснова Дарья Сергеевна": "14988",
    "Крыжко Дарья Александровна": "20091",
    "Купоров Юрий Юрьевич": "5383",
    "Лагутенков Алексей Александрович": "25040",
    "Люкевич Игорь Николаевич": "12430",
    "Меликян Арцрун Врежевич": "28802",
    "Митрофанова Валентина Андреевна": "28055",
    "Михель Екатерина Алексеевна": "17085",
    "Мокеева Татьяна Васильевна": "8557",
    "Неелова Наталья Владимировна": "4446",
    "Некрасова Татьяна Петровна": "4455",
    "Непряхина Татьяна Михайловна": "23057",
    "Покровская Любовь Леонидовна": "15009",
    "Родионов Дмитрий Григорьевич": "11408",
    "Рудская Ирина Андреевна": "6304",
    "Рытова Елена Владимировна": "16910",
    "Сорокожердьев Кирилл Геннадьевич": "277",
    "Степанова Ксения Сергеевна": "20342",
    "Степанчук Андрей Анатольевич": "12638",
    "Сулоева Светлана Борисовна": "6285",
    "Схведиани Анги Ерастиевич": "15249",
    "Танин Евгений Феофанович": "998466",
    "Тихомиров Антон Федорович": "6468",
    "Тутуева Дарья Дмитриевна": "27082",
    "Шиманова Дарья Андреевна": "24062",
    "Абдулаева Зинаида Игоревна": "17393",
    "Александрова Ариадна Иосифовна": "225",
    "Алферьев Дмитрий Александрович": "21689",
    "Воропаева Юлия Адольфовна": "1230",
    "Дунаенко Никита Алексеевич": "23744",
    "Ильяшенко Оксана Юрьевна": "12414",
    "Кравченко Валентина Витальевна": "12546",
    "Резанова Виктория Сергеевна": "25214",
    "Старченкова Олеся Дмитриевна": "25329",
    "Ферапонтова Анна Андреевна": "21660",
    "Филина Анна Валерьевна": "25461",
    "Фуртатова Алина Сергеевна": "22621",
    "Чекмарев Сергей Юрьевич": "23741",
    "Благова Ирина Юрьевна": "23640",
    "Власова Екатерина Алексеевна": "28397",
    "Давыдова Яна Сергеевна": "26063",
    "Иванова Наталья Васильевна": "14333",
    "Кудрявцева Татьяна Юрьевна": "3122",
    "Малашенко Марина Руслановна": "25337",
    "Новикова Ольга Валентиновна": "12150",
    "Норвардян Розалия Владимировна": "25158",
    "Панкова Людмила Владимировна": "99479",
    "Сергеев Дмитрий Анатольевич": "2662",
    "Смирнова Ольга Александровна": "5980",
    "Терешко Екатерина Кирилловна": "21818",
    "Томшинская Ирина Николаевна": "14331",
    "Якоб Полина Александровна": "25675",
  "Волобуева Анара Сергеевна": "27007",
"Майкова Анастасия Александровна": "998497",
"Бёттгер Кристиан": "26294",
"Шауя Цзигээр": "25298",
"Ниемб Бекуме Сюзанн": "20476",
"Чан Хоанг Хиеу": "26195",
"Ефремов Андрей Александрович": "25361",
"Зерари Раян": "998495",
"Пищалкина Илона Юрьевна": "999984",
"Соловьев Марк Владиславович": "998363",
"Тузников Михаил Алексеевич": "663",
"Кошеварова Анастасия Алексеевна": "998496",
"Арутюнян Маня Гайковна": "998126",
"Бахмутская Александра Викторовна": "999009",
"Бирюков Дмитрий Сергеевич": "999443",
"Бичевая Ольга Вячеславовна": "998309",
"Дерягина Александра Андреевна": "998473",
"Долгополова Елена Юрьевна": "998115",
"Калугин Александр Николаевич": "998155",
"Карлик Ефим Михайлович": "998119",
"Ткачук Николай Викторович": "998406",
"Пилецкая Лилия Сергеевна": "998017",
"Шевелева Ольга Борисовна": "26536",
"Соболев Даниил Васильевич": "998494",
"Перепечко Олеся Васильевна": "20590",
"Суровцев Максим Андреевич": "998514",
  "Орлов Егор Сергеевич": "5158",
"Сущенко Валерий Петрович": "6276",
"Авдуевская Екатерина Алексеевна": "16983",
"Акимова Юлия Николаевна": "22974",
"Александров Игорь Николаевич": "3459",
"Барабанов Антон Анатольевич": "22968",
"Воронова Ирина Владимировна": "25044",
"Горбунова Эллина Витальевна": "998263",
"Евтеева Екатерина Сергеевна": "998510",
"Демидов Михаил Олегович": "998443",
"Евсеева Светлана Анатольевна": "3194",
"Жогова Елена Вячеславовна": "17080",
"Иванов Федор Кириллович": "15294",
"Иванова Марина Вячеславовна": "15896",
"Кособоков Андрей Юрьевич": "23714",
"Краснов Сергей Васильевич": "99754",
"Кулькаев Григорий Александрович": "23359",
"Кулькаева Наталья Игоревна": "25284",
"Макарова Ольга Николаевна": "99905",
"Масюк Никита Александрович": "998465",
"Надёжина Ольга Сергеевна": "12524",
"Назарова Варвара Вадимовна": "23962",
"Попова Ольга Сергеевна": "998367",
"Путинцева Наталья Александровна": "21898",
"Рассказова Ольга Анатольевна": "4042",
"Родичев Максим Леонидович": "23055",
"Савекин Вадим Федорович": "998509",
"Танина Анна Валерьевна": "15883",
"Тимофеев Сергей Алексеевич": "14370",
"Третьякова Ирина Александровна": "26808",
"Уразаев Виктор Станиславович": "29737",
"Феофилова Татьяна Юрьевна": "99762",
"Швец Оксана Владимировна": "998511",
#"Попова Александра": ""
}

COMMISSION_MEMBERS: dict[str, list[str]] = {
    "Комса1": ["Иванов Иван Иванович", "Петров Пётр Петрович", "Смирнова Анна Сергеевна"],
    "Комса2": ["Иванов Иван Иванович", "Сидоров Сидор Сидорович"],
    "Комса3": ["Петров Пётр Петрович", "Кузнецова Елена Викторовна"],
    "Комса4": ["Смирнова Анна Сергеевна", "Попов Дмитрий Александрович"],
    "Комса5": ["Иванов Иван Иванович", "Кузнецова Елена Викторовна", "Васильев Сергей Николаевич"],
    "Комса6": ["Сидоров Сидор Сидорович", "Попов Дмитрий Александрович"],
    "Комса7": ["Васильев Сергей Николаевич", "Смирнова Анна Сергеевна"],
    "Комса8": ["Кузнецова Елена Викторовна", "Петров Пётр Петрович"],
    "Комса9": ["Попов Дмитрий Александрович", "Иванов Иван Иванович"],
    "Комса10": ["Васильев Сергей Николаевич", "Сидоров Сидор Сидорович", "Кузнецова Елена Викторовна"],
    "Комса11": ["Смирнова Анна Сергеевна", "Попов Дмитрий Александрович"],
    "Комса12": ["Петров Пётр Петрович", "Васильев Сергей Николаевич"]
}

def parse_place(place_element):
    if not place_element:
        return "Не указано"
    link = place_element.find('a', class_='lesson__link')
    if not link:
        return "Не указано"
    text = link.get_text(strip=True)
    text = re.sub(r'(\d)(ауд\.)', r'\1 \2', text)
    parts = [p.strip() for p in text.split(',') if p.strip()]
    return ', '.join(dict.fromkeys(parts))

def parse_sdo_link(lesson_element) -> str:
    """Извлекает ссылку СДО из lesson__resource_links."""
    if not lesson_element:
        return ""
    resource = lesson_element.find("div", class_="lesson__resource_links")
    if not resource:
        return ""
    link = resource.find("a", class_="lesson__link", href=True)
    if not link:
        return ""
    href = link.get("href", "").strip()
    # Иногда в href бывает двойной слеш — нормализуем
    if href.startswith("https://dl-imet.spbstu.ru//"):
        href = href.replace("https://dl-imet.spbstu.ru//", "https://dl-imet.spbstu.ru/", 1)
    return href

def parse_ruz_date_to_date(date_text: str, year: int = 2026) -> date | None:

    if not date_text:
        return None
    try:
       # s = str(date_text).lower().strip().split(",")[0].strip()
        s = str(date_text).lower().split(",")[0].strip()
        parts = s.split()
        if len(parts) < 2:
            return None
        day = int(parts[0])
      #  month_raw = parts[1].rstrip(".")  
        month_raw = parts[1].strip(". \t\n\r\xa0")

        months = {
           
            "января": 1, "февраля": 2, "марта": 3, "апреля": 4,
            "мая": 5, "июня": 6, "июля": 7, "августа": 8,
            "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12,
     #проверить сокращения когда откроется расписание
            "янв": 1, "фев": 2, "мар": 3, "апр": 4,
            "мая": 5, "июн": 6, "июл": 7, "авг": 8,
            "сент": 9,  "сент.": 9, "окт": 10, "нояб": 11, "нояб.": 11,"дек": 12,
        }
        month = months.get(month_raw)
        if not month:
            return None
        return date(year, month, day)
    except Exception:
        return None
        
def parse_group_schedule(group_human: str, start_date: datetime, end_date: datetime, show_progress: bool = True):
    if group_human not in GROUP_MAP:
        st.error(f"Группа {group_human} не найдена.")
        return pd.DataFrame()
    group_id = GROUP_MAP[group_human]
    all_lessons = []

    s = start_date.date() if isinstance(start_date, datetime) else start_date
    e = end_date.date() if isinstance(end_date, datetime) else end_date

    current = datetime.combine(s, datetime.min.time()) - timedelta(days=s.weekday())


    week_dates = []
    tmp = current
    while tmp.date() <= e:
        week_dates.append(tmp)
        tmp += timedelta(weeks=1)
    total_weeks = max(len(week_dates), 1)

    progress_bar = st.progress(0, text="0%") if show_progress else None
    week_count = 0

    for current in week_dates:
        week_count += 1
        url = f"https://ruz.spbstu.ru/faculty/100/groups/{group_id}?date={current.strftime('%Y-%m-%d')}"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for day in soup.find_all('li', class_='schedule__day'):
                    date_elem = day.find('div', class_='schedule__date')
                    if not date_elem:
                        continue
                    date_text = date_elem.text.strip()

                    try:
                        lesson_date = parse_ruz_date_to_date(date_text, year=2026)
                        if lesson_date is None:
                            continue
                        if lesson_date < s or lesson_date > e:
                            continue
                    except Exception:
                        continue

                    for lesson in day.find_all('li', class_='lesson'):
                   
                      time_str = ""
                      time_elem = lesson.find('span', class_='lesson__time')
                      if time_elem:
                          time_str = time_elem.get_text(strip=True)
                  
                      
                      subject = ""
                      subject_elem = lesson.find('div', class_='lesson__subject')
                      if subject_elem:
                         
                          time_in_subj = subject_elem.find('span', class_='lesson__time')
                          if time_in_subj:
                              time_in_subj.decompose()  
                          
                          subject = subject_elem.get_text(strip=True)
                          subject = re.sub(r'\s+', ' ', subject).strip()
                  
                     
                      lesson_type = lesson.find('div', class_='lesson__type')
                      lesson_type = lesson_type.get_text(strip=True) if lesson_type else ""
                  
                      
                      teachers = []
                      teachers_elem = lesson.find('div', class_='lesson__teachers')
                      if teachers_elem:
                          for a in teachers_elem.find_all('a'):
                              name = a.get_text(strip=True)
                              if name and len(name) > 3:
                                  teachers.append(name)
                  
                      teacher_str = ", ".join(teachers) if teachers else "Не указано"
                  
                     
                      place = parse_place(lesson.find('div', class_='lesson__places'))
                  
                      
                      if subject:
                          all_lessons.append({
                              "Дата": date_text,
                              "Время": time_str,
                              "Дисциплина": subject,
                              "Тип занятия": lesson_type,
                              "Преподаватель": teacher_str,
                              "Место": place,
                              "Группа": group_human,
                            "Ссылка": parse_sdo_link(lesson),
                          })

          

          
            if progress_bar is not None:
                pct = week_count / total_weeks
                progress_bar.progress(pct, text=f"{int(pct * 100)}%")
            time.sleep(2)
        except Exception as e:
            st.warning(f"Ошибка на неделе {current}: {e}")
            if progress_bar is not None:
                pct = week_count / total_weeks
                progress_bar.progress(pct, text=f"{int(pct * 100)}%")
    if progress_bar is not None:
        progress_bar.progress(1.0, text="100%")
    return pd.DataFrame(all_lessons)


def parse_teacher_schedule(teacher_name: str, start_date: datetime, end_date: datetime, show_progress: bool = True):
    if teacher_name not in TEACHER_MAP:
        st.error(f"Преподаватель {teacher_name} не найден.")
        return pd.DataFrame()
    teacher_id = TEACHER_MAP[teacher_name]
    all_lessons = []

    s = start_date.date() if isinstance(start_date, datetime) else start_date
    e = end_date.date() if isinstance(end_date, datetime) else end_date

    current = datetime.combine(s, datetime.min.time()) - timedelta(days=s.weekday())


    week_dates = []
    tmp = current
    while tmp.date() <= e:
        week_dates.append(tmp)
        tmp += timedelta(weeks=1)
    total_weeks = max(len(week_dates), 1)

    progress_bar = st.progress(0, text="0%") if show_progress else None
    week_count = 0
    base_url = f"https://ruz.spbstu.ru/teachers/{teacher_id}"

    for current in week_dates:
        week_count += 1
        url = f"{base_url}?date={current.strftime('%Y-%m-%d')}"
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for day in soup.find_all('li', class_='schedule__day'):
                    date_elem = day.find('div', class_='schedule__date')
                    if not date_elem:
                        continue
                    date_text = date_elem.text.strip()

                    try:
                        lesson_date = None
                        for fmt in ("%d.%m.%Y", "%d.%m.%y"):
                            try:
                                lesson_date = datetime.strptime(date_text.strip(), fmt).date()
                                break
                            except ValueError:
                                pass
                        if lesson_date is None:
                            lesson_date = parse_ruz_date_to_date(date_text, year=2026)
                        if lesson_date is None:
                            continue
                        if lesson_date < s or lesson_date > e:
                            continue
                    except Exception:
                        pass

                    for lesson in day.find_all('li', class_='lesson'):
                        subject = ""
                        subject_elem = lesson.find('div', class_='lesson__subject')
                        if subject_elem:
                            spans = subject_elem.find_all('span')
                            if spans and len(spans) > 2:
                                subject = spans[-1].text.strip()
                        lesson_type = lesson.find('div', class_='lesson__type')
                        lesson_type = lesson_type.text.strip() if lesson_type else ""
                        time_str = lesson.find('span', class_='lesson__time')
                        time_str = time_str.text.strip() if time_str else ""
                        groups = []
                        groups_elem = lesson.find('div', class_='lesson-groups__list')
                        if groups_elem:
                            for link in groups_elem.find_all('a', class_='lesson__link'):
                                groups.append(link.text.strip())
                        place = parse_place(lesson.find('div', class_='lesson__places'))

                        teacher_element = lesson.find('div', class_='lesson__teachers')
                        is_our_teacher = False
                        teacher_name_to_save = "Не указано"  
                        
                        if teacher_element:
                            teacher_links = teacher_element.find_all('a')
                            if any(f'/teachers/{teacher_id}' in a.get('href', '') for a in teacher_links):
                                is_our_teacher = True
                                
                                teacher_name_to_save = teacher_name 
                            else:
                               
                                is_our_teacher = False
                        else:
                           
                            is_our_teacher = True
                            
                        if is_our_teacher and subject:
                            all_lessons.append({
                                "Дата": date_text,
                                "Время": time_str,
                                "Дисциплина": subject,
                                "Тип занятия": lesson_type,
                                "Группы": ', '.join(groups),
                                "Преподаватель": teacher_name_to_save, 
                                "Место": place,
                              "Ссылка": parse_sdo_link(lesson),
                            })


          
            if progress_bar is not None:
                pct = week_count / total_weeks
                progress_bar.progress(pct, text=f"{int(pct * 100)}%")
            time.sleep(2)
        except Exception as e:
            st.warning(f"Ошибка на неделе {current}: {e}")
            if progress_bar is not None:
                pct = week_count / total_weeks
                progress_bar.progress(pct, text=f"{int(pct * 100)}%")
    if progress_bar is not None:
        progress_bar.progress(1.0, text="100%")
    return pd.DataFrame(all_lessons)

def generate_time_slots(start: date | datetime, end: date | datetime, hours: range = range(8, 21)) -> list[datetime]:
    if isinstance(start, date) and not isinstance(start, datetime):
        start = datetime.combine(start, datetime.min.time())
    if isinstance(end, date) and not isinstance(end, datetime):
        end = datetime.combine(end, datetime.min.time())

    slots = []
    current = start.replace(hour=8, minute=0, second=0, microsecond=0)
    while current.date() <= end.date():
        for h in hours:
            slot = current.replace(hour=h)
            if slot.date() > end.date():
                break
            slots.append(slot)
        current += timedelta(days=1)
    return slots


def build_empty_matrix(time_slots: list[datetime], commission_names: list[str]) -> pd.DataFrame:
    slot_labels = [s.strftime("%d.%m %H:%M") for s in time_slots]
    df = pd.DataFrame(index=slot_labels, columns=commission_names)
    df[:] = ""
    return df


def auto_mark_conflicts(matrix: pd.DataFrame, commission_members: dict) -> pd.DataFrame:

    if matrix is None or matrix.empty:
        return pd.DataFrame()
    
    result_df = matrix.copy().astype(str).fillna("")
    
    comms = list(result_df.columns)
    
    # Для каждого временного слота (строки)
    for idx in result_df.index:
        busy_members = set()   

        for comm in comms:
            cell_value = result_df.loc[idx, comm]
            if cell_value and cell_value != "nan" and "🟢" not in cell_value:
              
                busy_members.update(commission_members.get(comm, []))
        

        for comm in comms:
            comm_members = set(commission_members.get(comm, []))
                       
            if comm_members & busy_members:
                current_value = result_df.loc[idx, comm]
              
                if pd.isna(current_value) or current_value == "" or current_value == "nan":
                    result_df.loc[idx, comm] = "🟢 Занято"
               
                elif "🟢" not in current_value and "🔴" not in current_value:
                    result_df.loc[idx, comm] = f"🟢 {current_value}"
    
    return result_df

def combine_teachers(x):
    teachers = sorted(set(str(n).strip() for n in x.dropna() if str(n).strip() and str(n).strip() != "Не указано"))
    return ", ".join(teachers) if teachers else "Не указано"

def prepare_export_dataframe(combined_df: pd.DataFrame) -> pd.DataFrame:
    if combined_df.empty:
        return pd.DataFrame()

    df = combined_df.copy()

    # Нормализация групп
    if "Группы" in df.columns and "Группа" not in df.columns:
        df["Группа"] = df["Группы"].str.split(r',\s*')
        df = df.explode("Группа")
    elif "Группа" not in df.columns:
        return pd.DataFrame()

    df["Тип занятия"] = df["Тип занятия"].str.strip()

    # --- агрегация ---
    def combine_links(x):
        links = sorted({str(u).strip() for u in x.dropna() if str(u).strip()})
        return ", ".join(links) if links else ""

    agg_dict = {
        "Преподаватель": combine_teachers,
        "Место": lambda x: ", ".join(sorted(set(x.dropna()))),
        "Тип занятия": lambda x: x.value_counts().to_dict(),
    }

    # Если столбец Ссылка есть — добавляем его в агрегацию
    if "Ссылка" in df.columns:
        agg_dict["Ссылка"] = combine_links

    grouped = df.groupby(["Группа", "Дисциплина"], as_index=False).agg(agg_dict)

    type_counts = grouped["Тип занятия"].apply(pd.Series).fillna(0).astype(int)
    grouped = grouped.drop(columns=["Тип занятия"])
    result = pd.concat([grouped, type_counts], axis=1)

    result.insert(2, "Контроль", "")

    preferred_type_order = [
        "Лекции", "Практика", "Практическое занятие", "Семинар",
        "Консультация", "Экзамен", "Зачёт", "Зачет",
    ]

    cols = result.columns.tolist()
    for c in ("Преподаватель", "Место", "Ссылка"):
        if c in cols:
            cols.remove(c)

    fixed = ["Группа", "Дисциплина", "Контроль"]
    other_types = [t for t in preferred_type_order if t in cols and t not in fixed]
    other_types += [c for c in cols if c not in fixed and c not in other_types]

    final_cols = fixed + other_types + ["Преподаватель", "Место"]
    if "Ссылка" in result.columns:
        final_cols.append("Ссылка")          # ← последний столбец

    final_cols = [c for c in final_cols if c in result.columns]
    result = result[final_cols]

    result.rename(columns={"Место": "Формат занятий"}, inplace=True)
    return result

def prepare_sorted_raw_sheets(
    combined_df: pd.DataFrame,
    selected_groups: list[str] | None = None,
    selected_teachers: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
 
    if combined_df is None or combined_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    df = combined_df.copy()

    def _to_dt(x):
        d = parse_ruz_date_to_date(x, 2026)
        if d is not None:
            return d
        for fmt in ("%d.%m.%Y", "%d.%m.%y"):
            try:
                return datetime.strptime(str(x).strip(), fmt).date()
            except ValueError:
                pass
        return None

    df["_dt"] = df["Дата"].apply(_to_dt)

    selected_groups = selected_groups or []
    selected_teachers = selected_teachers or []


    gdf = pd.DataFrame()
    if "Группа" in df.columns and selected_groups:
        mask_group = df["Группа"].isin(selected_groups)
        if "Группы" in df.columns:
            mask_group = mask_group & (
                df["Группы"].isna() | (df["Группы"].astype(str).str.strip() == "")
            )
        gdf = df[mask_group].copy()
        gdf = gdf.dropna(subset=["_dt"]).sort_values(
            by=["_dt", "Группа", "Время"],
            ascending=[True, True, True],  # дата: от ранней к поздней
        )
        gdf = gdf.drop(columns=["_dt"], errors="ignore")

        preferred = ["Группа", "Дата", "Время", "Дисциплина", "Тип занятия", "Преподаватель", "Место"]
        cols = [c for c in preferred if c in gdf.columns] + [
            c for c in gdf.columns if c not in preferred and c not in ("Группы",)
        ]
        gdf = gdf[cols]

        extra_rows = []


        teachers_from_groups = sorted(
            set(
                t.strip()
                for cell in gdf.get("Преподаватель", pd.Series(dtype=str)).dropna()
                for t in str(cell).split(",")
                if t.strip()
            )
        )
        if teachers_from_groups:
            empty = {c: "" for c in gdf.columns}
            header_row = {c: "" for c in gdf.columns}
            header_row[gdf.columns[0]] = (
                "Преподаватели, которые ведут занятия у этих групп в указанный период"
            )
            extra_rows.extend([empty, header_row])
            for name in teachers_from_groups:
                row = {c: "" for c in gdf.columns}
                row[gdf.columns[0]] = name
                extra_rows.append(row)

  
        if "Тип занятия" in gdf.columns and not gdf.empty:
          
            type_counts = (
                gdf["Тип занятия"]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", pd.NA)
                .dropna()
                .value_counts()
            )
            if not type_counts.empty:
                empty = {c: "" for c in gdf.columns}
                header_row = {c: "" for c in gdf.columns}
                header_row[gdf.columns[0]] = "Статистика по типам занятий"
                extra_rows.extend([empty, header_row])
                for typ, cnt in type_counts.items():
                    row = {c: "" for c in gdf.columns}
                    row[gdf.columns[0]] = str(typ)
                    # второй столбец — количество
                    if len(gdf.columns) > 1:
                        row[gdf.columns[1]] = int(cnt)
                    extra_rows.append(row)

        if extra_rows:
            gdf = pd.concat([gdf, pd.DataFrame(extra_rows)], ignore_index=True)

 
    tdf = pd.DataFrame()
    if selected_teachers and "Преподаватель" in df.columns:

        def teacher_match(cell):
            if pd.isna(cell):
                return False
            names = [x.strip() for x in str(cell).split(",")]
            return any(t in selected_teachers for t in names)

        tdf = df[df["Преподаватель"].apply(teacher_match)].copy()

        if "Группы" in tdf.columns:
            tdf = tdf[tdf["Группы"].notna() & (tdf["Группы"].astype(str).str.strip() != "")]

        tdf = tdf[
            tdf["Преподаватель"].apply(
                lambda x: any(t == str(x).strip() for t in selected_teachers)
            )
        ]

        tdf = tdf.dropna(subset=["_dt"]).sort_values(
            by=["Преподаватель", "_dt", "Время"],
            ascending=[True, False, True],  # ФИО ↑, дата ↓ (май→март), время ↑
        )
        
        tdf = tdf.drop(columns=["_dt"], errors="ignore")

        preferred = ["Преподаватель", "Дата", "Время", "Дисциплина", "Тип занятия", "Группы", "Место"]
        cols = [c for c in preferred if c in tdf.columns] + [
            c for c in tdf.columns if c not in preferred and c != "Группа"
        ]
        tdf = tdf[cols]

    return gdf, tdf
    
def format_header(members: list[str]) -> str:
    short = []
    for m in members:
        parts = m.split()
        if len(parts) >= 3:
            short.append(f"{parts[0]} {parts[1][0]}.{parts[2][0]}.")
        elif len(parts) >= 2:
            short.append(f"{parts[0]} {parts[1][0]}.")
        else:
            short.append(m)
    return ", ".join(short)


def display_schedule_by_date(df: pd.DataFrame, title: str = ""):
    if df.empty:
        st.info("Нет данных")
        return

    df_copy = df.copy()

    def parse_ruz_date(date_str):
        d = parse_ruz_date_to_date(date_str, year=2026)
        if d is None:
            for fmt in ("%d.%m.%Y", "%d.%m.%y"):
                try:
                    return pd.Timestamp(datetime.strptime(str(date_str).strip(), fmt))
                except ValueError:
                    pass
            return pd.NaT
        return pd.Timestamp(d)

    df_copy['Дата_parsed'] = df_copy['Дата'].apply(parse_ruz_date)

    if df_copy['Дата_parsed'].isna().all():
        st.warning("Не удалось распознать даты. Проверьте формат.")
        st.write("Примеры значений в столбце 'Дата':", df_copy['Дата'].head(10).tolist())
        return

    df_valid = df_copy.dropna(subset=['Дата_parsed']).sort_values(by='Дата_parsed')
    if df_valid.empty:
        st.warning("Нет корректных дат для отображения")
        return

    if title:
        st.subheader(title)

    for dt in df_valid['Дата_parsed'].unique():
        date_header = pd.Timestamp(dt).strftime("%d.%m.%Y")
        st.subheader(f"📅 {date_header}")
        day_data = df_valid[df_valid['Дата_parsed'] == dt].drop(columns=['Дата_parsed'])
        st.dataframe(day_data, use_container_width=True)


def build_summary_report(combined_df, selected_groups, selected_teachers, start_date, end_date):
    rows = [
        {"Параметр": "Всего занятий", "Значение": len(combined_df) if combined_df is not None else 0},
        {"Параметр": "Выбранные группы", "Значение": ", ".join(selected_groups) if selected_groups else "—"},
        {"Параметр": "Выбранные преподаватели", "Значение": ", ".join(selected_teachers) if selected_teachers else "—"},
    ]
    return pd.DataFrame(rows)





def parse_lesson_time(time_str):
    """Парсит строку времени '10:00–11:40' в (time_start, time_end)"""
    if not time_str or not isinstance(time_str, str):
        return None, None
    time_str = time_str.replace('–', '-').replace('—', '-').replace('−', '-')
    parts = time_str.split('-')
    if len(parts) != 2:
        return None, None
    try:
        from datetime import time as dt_time
        h1, m1 = map(int, parts[0].strip().split(':'))
        h2, m2 = map(int, parts[1].strip().split(':'))
        return dt_time(h1, m1), dt_time(h2, m2)
    except Exception:
        return None, None


def get_busy_intervals_for_day(lessons_df, day_date, work_start=None, work_end=None):
    from datetime import time as dt_time
    
    if work_start is None:
        from datetime import time as dt_time
        work_start = dt_time(10, 0)
    if work_end is None:
        from datetime import time as dt_time
        work_end = dt_time(20, 0)

    if lessons_df is None or lessons_df.empty:
        return []
    if 'Дата_parsed' not in lessons_df.columns:
        return []

    day_lessons = lessons_df[lessons_df['Дата_parsed'] == day_date]
    if day_lessons.empty:
        return []

    intervals = []
    for _, row in day_lessons.iterrows():
        t_start, t_end = parse_lesson_time(row['Время'])
        if t_start and t_end:
            dt_start = datetime.combine(day_date, t_start)
            dt_end = datetime.combine(day_date, t_end)
            intervals.append((dt_start, dt_end))

    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = []
    for s, e in intervals:
        if not merged or s > merged[-1][1]:
            merged.append([s, e])
        else:
            merged[-1][1] = max(merged[-1][1], e)

    # Ограничиваем рабочим днём
   
    
    day_start = datetime.combine(day_date, work_start)
    day_end = datetime.combine(day_date, work_end)
    result = []
    for s, e in merged:
        s = max(s, day_start)
        e = min(e, day_end)
        if s < e:
            result.append((s, e))
    return result


def find_common_free_windows(all_schedules, participants, start_date, end_date,
                            min_duration_td, weekdays_only, mode, min_free_count,
                            required_participants):
    """Основная логика поиска свободных окон"""
    results = []
    current = start_date.date() if isinstance(start_date, datetime) else start_date
    end = end_date.date() if isinstance(end_date, datetime) else end_date

    while current <= end:
        if weekdays_only and current.weekday() >= 5:
            current += timedelta(days=1)
            continue

        # Занятые интервалы для каждого участника
        participant_busy = {}
        for p in participants:
            df = all_schedules.get(p, pd.DataFrame())
            participant_busy[p] = get_busy_intervals_for_day(df, current)

        # Собираем все граничные точки
        all_points = set()
        from datetime import time as dt_time
        day_start = datetime.combine(current, dt_time(10, 0))
        day_end = datetime.combine(current, dt_time(20, 0))
        all_points.add(day_start)
        all_points.add(day_end)

        for p in participants:
            for s, e in participant_busy[p]:
                all_points.add(s)
                all_points.add(e)

        sorted_points = sorted(all_points)

        # Проверяем каждый микро-интервал
        valid_segments = []
        for i in range(len(sorted_points) - 1):
            seg_start = sorted_points[i]
            seg_end = sorted_points[i + 1]
            if seg_start >= seg_end:
                continue

            free_count = 0
            busy_list = []
            required_ok = True

            for p in participants:
                is_free = True
                for s, e in participant_busy[p]:
                    if s < seg_end and e > seg_start:
                        is_free = False
                        break
                if is_free:
                    free_count += 1
                else:
                    busy_list.append(p)
                    if p in required_participants:
                        required_ok = False

            if not required_ok:
                continue
            if mode == "hard" and free_count != len(participants):
                continue
            if mode == "soft" and free_count < min_free_count:
                continue

            valid_segments.append({
                'seg_start': seg_start,
                'seg_end': seg_end,
                'free_count': free_count,
                'busy_participants': busy_list,
            })

        day_windows = merge_valid_segments(valid_segments, min_duration_td)
        for w in day_windows:
            w['date'] = current
            w['total_count'] = len(participants)
            results.append(w)

        current += timedelta(days=1)

    return results

def ceil_hour(dt):
    """Округляет datetime вверх до ближайшего целого часа"""
    if dt.minute == 0 and dt.second == 0 and dt.microsecond == 0:
        return dt
    return dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)


def floor_hour(dt):
    """Округляет datetime вниз до ближайшего целого часа"""
    return dt.replace(minute=0, second=0, microsecond=0)


def add_parsed_date(df):
    """Добавляет колонку Дата_parsed к датафрейму расписания"""
    if df is None or df.empty or 'Дата_parsed' in df.columns:
        return df
    df = df.copy()

    def _try_parse(x):
        d = parse_ruz_date_to_date(x, 2026)
        if d is not None:
            return d
        for fmt in ("%d.%m.%Y", "%d.%m.%y"):
            try:
                return datetime.strptime(str(x).strip(), fmt).date()
            except ValueError:
                pass
        return None

    df['Дата_parsed'] = df['Дата'].apply(_try_parse)
    return df


def merge_valid_segments(segments, min_duration_td):
    """Объединяет соседние валидные сегменты с одинаковым набором занятых участников"""
    if not segments:
        return []

    segments = sorted(segments, key=lambda x: x['seg_start'])
    merged = []
    current = {
        'seg_start': segments[0]['seg_start'],
        'seg_end': segments[0]['seg_end'],
        'free_count': segments[0]['free_count'],
        'busy_participants': set(segments[0]['busy_participants']),
    }

    for seg in segments[1:]:
        busy_set = set(seg['busy_participants'])
        if seg['seg_start'] == current['seg_end'] and busy_set == current['busy_participants']:
            current['seg_end'] = seg['seg_end']
        else:
            nice_start = ceil_hour(current['seg_start'])
            nice_end = floor_hour(current['seg_end'])
            if nice_start < nice_end and (nice_end - nice_start) >= min_duration_td:
                merged.append({
                    'real_start': current['seg_start'],
                    'real_end': current['seg_end'],
                    'nice_start': nice_start,
                    'nice_end': nice_end,
                    'free_count': current['free_count'],
                    'busy_participants': sorted(current['busy_participants']),
                })
            current = {
                'seg_start': seg['seg_start'],
                'seg_end': seg['seg_end'],
                'free_count': seg['free_count'],
                'busy_participants': busy_set,
            }

    nice_start = ceil_hour(current['seg_start'])
    nice_end = floor_hour(current['seg_end'])
    if nice_start < nice_end and (nice_end - nice_start) >= min_duration_td:
        merged.append({
            'real_start': current['seg_start'],
            'real_end': current['seg_end'],
            'nice_start': nice_start,
            'nice_end': nice_end,
            'free_count': current['free_count'],
            'busy_participants': sorted(current['busy_participants']),
        })

    return merged


def get_lesson_context(lessons_df, day_date, window_time, position='before'):
    """Возвращает строку с ближайшим занятием до или после окна"""
    if lessons_df is None or lessons_df.empty:
        return "нет занятий в этот день"
    if 'Дата_parsed' not in lessons_df.columns:
        return "нет занятий в этот день"

    day_lessons = lessons_df[lessons_df['Дата_parsed'] == day_date]
    if day_lessons.empty:
        return "нет занятий в этот день"

    lessons_parsed = []
    for _, row in day_lessons.iterrows():
        t_start, t_end = parse_lesson_time(row['Время'])
        if t_start and t_end:
            dt_start = datetime.combine(day_date, t_start)
            dt_end = datetime.combine(day_date, t_end)
            lessons_parsed.append({'start': dt_start, 'end': dt_end, 'row': row})

    if not lessons_parsed:
        return "нет занятий в этот день"

    if position == 'before':
        candidates = [l for l in lessons_parsed if l['end'] <= window_time]
        if not candidates:
            return "нет занятий до окна"
        closest = max(candidates, key=lambda x: x['end'])
    else:
        candidates = [l for l in lessons_parsed if l['start'] >= window_time]
        if not candidates:
            return "нет занятий после окна"
        closest = min(candidates, key=lambda x: x['start'])

    row = closest['row']
    time_str = row['Время']
    subject = row['Дисциплина']
    place = row.get('Место', 'Не указано')

    if 'Группа' in row and pd.notna(row['Группа']) and str(row['Группа']).strip():
        teacher = row.get('Преподаватель', 'Не указано')
        return f"{time_str} {subject} ({teacher}) · {place}"
    else:
        groups = row.get('Группы', 'Не указано')
        return f"{time_str} {subject} (гр. {groups}) · {place}"

# =====================================================================
# ⚖️ ПЛАНИРОВАНИЕ ГИА (защиты ВКР) – НОВЫЙ БЛОК (версия 2)
# Вставить ЦЕЛИКОМ перед строкой:
#     tab1, tab2, tab3, tab4, tab5 = st.tabs([
# Использует GROUP_MAP и TEACHER_MAP, объявленные выше в app.py.
# =====================================================================
import json
import os
import uuid
from datetime import time as dtime

GIA_LOCAL_FILE = "gia_data.json"          # локальная копия на сервере Streamlit
GIA_COMM_COLS = ["Комиссия", "ФИО"]
GIA_SESS_COLS = ["ID", "Комиссия", "Дата", "Начало", "Длительность, мин", "Группа"]
GIA_DEFAULT_PARAMS = {
    "start": "2027-06-01", "end": "2027-06-30",
    "hour_from": 8, "hour_to": 20, "step": 30,
    "weekends": False, "only_busy_days": True,
}
GIA_DURATIONS = list(range(30, 601, 30))  # 30 мин – 10 ч


# ---------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------
def _gia_short(fio: str) -> str:
    """Иванов Иван Иванович -> Иванов И. И."""
    parts = str(fio).split()
    if len(parts) < 2 or not all(x.replace("-", "").isalpha() for x in parts[1:3]) or parts[1].endswith("."):
        return str(fio)
    if len(parts) >= 3:
        return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
    if len(parts) == 2:
        return f"{parts[0]} {parts[1][0]}."
    return str(fio)


def _gia_dur_label(m: int) -> str:
    h, mm = divmod(int(m), 60)
    if h and mm:
        return f"{h} ч {mm} мин"
    return f"{h} ч" if h else f"{mm} мин"


def _gia_parse_date(v) -> date | None:
    if v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip() in ("", "nan", "NaT", "None"):
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = str(v).strip()
    try:
        return date.fromisoformat(s[:10])
    except ValueError:
        try:
            return pd.to_datetime(s, dayfirst=True).date()
        except Exception:
            return None


def _gia_parse_time(v) -> dtime | None:
    if v is None or str(v).strip() in ("", "nan", "NaT", "None"):
        return None
    if isinstance(v, dtime):
        return v.replace(second=0, microsecond=0)
    if isinstance(v, datetime):
        return v.time().replace(second=0, microsecond=0)
    m = re.match(r"^\s*(\d{1,2})[:.](\d{2})", str(v))
    if not m:
        return None
    h, mi = int(m.group(1)), int(m.group(2))
    return dtime(h, mi) if 0 <= h < 24 and 0 <= mi < 60 else None


def _gia_canonical_name(name: str) -> str:
    """Убирает лишние пробелы; если ФИО есть в TEACHER_MAP — берёт написание оттуда."""
    clean = " ".join(str(name).replace("ё", "е").split()).strip()
    if not clean:
        return ""
    for t in TEACHER_MAP.keys():
        if " ".join(t.replace("ё", "е").split()).lower() == clean.lower():
            return t
    return " ".join(str(name).split()).strip()


GIA_RU_WD = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
GIA_DEFAULT_START = "10:00"
GIA_DEFAULT_DUR = 120


def _gia_normalize(comm: pd.DataFrame, sess: pd.DataFrame, params: dict):
    """Приводит данные к единому виду (строки, ISO-даты, ЧЧ:ММ).
    Строка заседания может быть без даты – это «план»: ГЭК и группа есть, дата ещё не выбрана."""
    comm = comm.copy() if comm is not None else pd.DataFrame(columns=GIA_COMM_COLS)
    for c in GIA_COMM_COLS:
        if c not in comm.columns:
            comm[c] = ""
    comm = comm[GIA_COMM_COLS].fillna("").astype(str)
    comm["Комиссия"] = comm["Комиссия"].str.strip()
    comm["ФИО"] = comm["ФИО"].apply(lambda x: _gia_canonical_name(x) if str(x).strip() else "")
    comm = comm[comm["Комиссия"] != ""].drop_duplicates().reset_index(drop=True)
    # у комиссии с людьми убираем пустую строку-заглушку
    has_people = set(comm.loc[comm["ФИО"] != "", "Комиссия"])
    comm = comm[~((comm["ФИО"] == "") & comm["Комиссия"].isin(has_people))].reset_index(drop=True)
    order = {c: i for i, c in enumerate(dict.fromkeys(comm["Комиссия"]))}

    sess = sess.copy() if sess is not None else pd.DataFrame(columns=GIA_SESS_COLS)
    for c in GIA_SESS_COLS:
        if c not in sess.columns:
            sess[c] = ""
    rows = []
    for _, r in sess.iterrows():
        comm_name = "" if pd.isna(r["Комиссия"]) else str(r["Комиссия"]).strip()
        if not comm_name or comm_name == "nan":
            continue
        d = _gia_parse_date(r["Дата"])
        t = _gia_parse_time(r["Начало"]) or _gia_parse_time(GIA_DEFAULT_START)
        try:
            dur = int(float(r["Длительность, мин"]))
        except (TypeError, ValueError):
            dur = GIA_DEFAULT_DUR
        rid = "" if pd.isna(r["ID"]) else str(r["ID"]).strip()
        grp = "" if pd.isna(r["Группа"]) else str(r["Группа"]).strip()
        rows.append({
            "ID": rid if rid and rid not in ("nan", "None") else uuid.uuid4().hex[:8],
            "Комиссия": comm_name,
            "Дата": d.isoformat() if d else "",
            "Начало": t.strftime("%H:%M"),
            "Длительность, мин": min(max(dur, 15), 720),
            "Группа": "" if grp in ("nan", "None") else grp,
        })
    # у каждой комиссии должна быть хотя бы одна строка – чтобы было куда вписать дату
    present = {r["Комиссия"] for r in rows}
    for c in order:
        if c not in present:
            rows.append({"ID": uuid.uuid4().hex[:8], "Комиссия": c, "Дата": "", "Начало": GIA_DEFAULT_START,
                         "Длительность, мин": GIA_DEFAULT_DUR, "Группа": ""})
    sess = pd.DataFrame(rows, columns=GIA_SESS_COLS)
    if not sess.empty:
        sess["_o"] = sess["Комиссия"].map(lambda c: order.get(c, 10_000))
        sess["_d"] = sess["Дата"].replace("", "9999-12-31")
        sess = sess.sort_values(["_o", "_d", "Начало", "Группа"]).drop(columns=["_o", "_d"]).reset_index(drop=True)

    p = dict(GIA_DEFAULT_PARAMS)
    for k, v in (params or {}).items():
        if k in p and str(v).strip() not in ("", "nan"):
            p[k] = v
    for k in ("hour_from", "hour_to", "step"):
        p[k] = int(float(p[k]))
    for k in ("weekends", "only_busy_days"):
        p[k] = str(p[k]).strip().lower() in ("true", "1", "да", "yes")
    p["start"] = (_gia_parse_date(p["start"]) or date.fromisoformat(GIA_DEFAULT_PARAMS["start"])).isoformat()
    p["end"] = (_gia_parse_date(p["end"]) or date.fromisoformat(GIA_DEFAULT_PARAMS["end"])).isoformat()
    return comm, sess, p


def _gia_commissions() -> list[str]:
    return list(dict.fromkeys(st.session_state.gia_comm["Комиссия"].tolist()))


def _gia_members() -> dict[str, list[str]]:
    """Состав каждой комиссии в порядке ввода; первый – председатель."""
    res = {c: [] for c in _gia_commissions()}
    for _, r in st.session_state.gia_comm.iterrows():
        if r["ФИО"] and r["ФИО"] not in res.setdefault(r["Комиссия"], []):
            res[r["Комиссия"]].append(r["ФИО"])
    return res


def _gia_chair(members: dict, c: str) -> str:
    lst = members.get(c, [])
    return lst[0] if lst else ""


def _gia_dated(sess: pd.DataFrame) -> pd.DataFrame:
    return sess[sess["Дата"].astype(str).str.strip() != ""]


def _gia_interval(r) -> tuple[datetime, datetime]:
    d = date.fromisoformat(r["Дата"])
    t = _gia_parse_time(r["Начало"]) or _gia_parse_time(GIA_DEFAULT_START)
    start = datetime.combine(d, t)
    return start, start + timedelta(minutes=int(r["Длительность, мин"]))


# ---------------------------------------------------------------------
# Ввод составов одним текстом
# ---------------------------------------------------------------------
GIA_ROLE_PREFIXES = ("председател", "зам", "секретар", "член", "состав", "эксперт")


def _gia_split_names(s: str) -> list[str]:
    return [x.strip() for x in re.split(r"[;,]+", s) if x.strip()]


def _gia_parse_text(text: str):
    """Разбирает текст вида
         ГЭК 1:
         Группа: в3743801/41401          (необязательно)
         Председатель 1
         Иванов Иван Иванович
    Возвращает (список комиссий, предупреждения). Первый человек в списке – председатель."""
    blocks, warns = [], []
    cur = None
    for raw in str(text).splitlines():
        line = raw.replace("\u200b", "").replace("\xa0", " ").strip()
        if not line:
            continue
        line = re.sub(r"^(\d{1,3}[.)]|[-–—•*·])\s*", "", line).strip()
        if not line:
            continue
        if ":" in line:
            head, rest = line.split(":", 1)
            hl = head.strip().lower().replace("ё", "е")
            if hl.startswith("групп"):
                if cur is None:
                    warns.append(f"Строка «{line}» стоит до названия комиссии – пропущена.")
                    continue
                cur["groups"] += [g for g in re.split(r"[,;\s]+", rest) if g.strip()]
                continue
            if hl.startswith(GIA_ROLE_PREFIXES):
                if cur is None:
                    warns.append(f"Строка «{line}» стоит до названия комиссии – пропущена.")
                    continue
                cur["members"] += _gia_split_names(rest)
                continue
            name = " ".join(head.split())
            cur = next((b for b in blocks if b["name"] == name), None)
            if cur is None:
                cur = {"name": name, "members": [], "groups": []}
                blocks.append(cur)
            cur["members"] += _gia_split_names(rest)
        else:
            if cur is None:
                warns.append(f"Строка «{line}» стоит до названия комиссии (нет строки вида «ГЭК 1:») – пропущена.")
                continue
            cur["members"].append(line)
    for b in blocks:
        seen = []
        for m in b["members"]:
            m = _gia_canonical_name(m)
            if m and m not in seen:
                seen.append(m)
        b["members"] = seen
        b["groups"] = list(dict.fromkeys(g.strip() for g in b["groups"] if g.strip()))
        if not b["members"]:
            warns.append(f"В «{b['name']}» не указано ни одного человека.")
    return blocks, warns


def _gia_text_from_data() -> str:
    members = _gia_members()
    sess = st.session_state.gia_sess
    out = []
    for c in _gia_commissions():
        out.append(f"{c}:")
        groups = [g for g in dict.fromkeys(sess.loc[sess["Комиссия"] == c, "Группа"]) if g]
        if groups:
            out.append("Группа: " + ", ".join(groups))
        out += members.get(c, [])
        out.append("")
    return "\n".join(out).strip()


def _gia_apply_text(widget_key: str):
    """Колбэк: срабатывает, когда курсор уходит из поля (или Ctrl+Enter)."""
    text = st.session_state.get(widget_key, "")
    blocks, warns = _gia_parse_text(text)
    if not blocks:
        st.session_state.gia_flash_warn = (
            ["Не найдено ни одной комиссии. Каждая комиссия начинается со строки с двоеточием, например «ГЭК 1:»."]
            + warns)
        return
    comm_rows = []
    for b in blocks:
        comm_rows += [{"Комиссия": b["name"], "ФИО": m} for m in b["members"]] or [{"Комиссия": b["name"], "ФИО": ""}]
    st.session_state.gia_comm = pd.DataFrame(comm_rows, columns=GIA_COMM_COLS)

    sess = st.session_state.gia_sess.copy()
    names = {b["name"] for b in blocks}
    # строки без даты у комиссий, которых больше нет, убираем; строки с датой оставляем (вдруг опечатка)
    sess = sess[sess["Комиссия"].isin(names) | (sess["Дата"] != "")].reset_index(drop=True)
    add = []
    for b in blocks:
        for g in b["groups"]:
            mine = sess["Комиссия"] == b["name"]
            if ((sess["Группа"] == g) & mine).any():
                continue
            free = sess.index[mine & (sess["Группа"] == "")]
            if len(free):
                sess.loc[free[0], "Группа"] = g
            else:
                add.append({"ID": uuid.uuid4().hex[:8], "Комиссия": b["name"], "Дата": "",
                            "Начало": GIA_DEFAULT_START, "Длительность, мин": GIA_DEFAULT_DUR, "Группа": g})
    if add:
        sess = pd.concat([sess, pd.DataFrame(add)], ignore_index=True)
    st.session_state.gia_sess = sess
    st.session_state.gia_flash_warn = warns
    _gia_commit(f"✅ Составы сохранены: комиссий – {len(blocks)}, "
                f"человек – {len({m for b in blocks for m in b['members']})}")


# ---------------------------------------------------------------------
# Пересечения
# ---------------------------------------------------------------------
def _gia_conflicts_for(cand: dict, sess: pd.DataFrame, members: dict, exclude_id: str | None = None) -> list[str]:
    out = []
    if not str(cand.get("Дата", "")).strip():
        return out
    try:
        c_start, c_end = _gia_interval(cand)
    except Exception:
        return out
    c_mem = set(members.get(cand["Комиссия"], []))
    for _, r in _gia_dated(sess).iterrows():
        if exclude_id is not None and r["ID"] == exclude_id:
            continue
        s, e = _gia_interval(r)
        if not (c_start < e and s < c_end):
            continue
        when = f"{s.strftime('%d.%m.%Y')} {s.strftime('%H:%M')}–{e.strftime('%H:%M')}"
        grp = f", гр. {r['Группа']}" if r["Группа"] else ""
        if r["Комиссия"] == cand["Комиссия"]:
            out.append(f"{r['Комиссия']} уже заседает {when}{grp}")
            continue
        for person in sorted(c_mem & set(members.get(r["Комиссия"], []))):
            out.append(f"{_gia_short(person)} занят(а) {when} ({r['Комиссия']}{grp})")
    return out


def _gia_all_conflicts(sess: pd.DataFrame, members: dict) -> dict[str, list[str]]:
    return {r["ID"]: _gia_conflicts_for(r.to_dict(), sess, members, exclude_id=r["ID"]) for _, r in sess.iterrows()}


# ---------------------------------------------------------------------
# Таблицы-результаты
# ---------------------------------------------------------------------
def _gia_summary(sess: pd.DataFrame, members: dict) -> pd.DataFrame:
    conf = _gia_all_conflicts(sess, members)
    rows = []
    for _, r in _gia_dated(sess).iterrows():
        s, e = _gia_interval(r)
        rows.append({
            "Дата": s.strftime("%d.%m.%Y"),
            "Время": f"{s.strftime('%H:%M')}–{e.strftime('%H:%M')}",
            "Комиссия": r["Комиссия"],
            "Группа": r["Группа"],
            "Председатель": _gia_chair(members, r["Комиссия"]),
            "Члены комиссии": "; ".join(members.get(r["Комиссия"], [])),
            "Пересечения": "; ".join(conf.get(r["ID"], [])) or "нет",
        })
    return pd.DataFrame(rows, columns=["Дата", "Время", "Комиссия", "Группа", "Председатель",
                                       "Члены комиссии", "Пересечения"])


def _gia_by_person(sess: pd.DataFrame, members: dict) -> pd.DataFrame:
    rows = []
    for _, r in _gia_dated(sess).iterrows():
        s, e = _gia_interval(r)
        for p in members.get(r["Комиссия"], []):
            rows.append({"ФИО": p, "Дата": s.strftime("%d.%m.%Y"), "_sort": s,
                         "Время": f"{s.strftime('%H:%M')}–{e.strftime('%H:%M')}",
                         "Комиссия": r["Комиссия"], "Группа": r["Группа"]})
    df = pd.DataFrame(rows, columns=["ФИО", "Дата", "_sort", "Время", "Комиссия", "Группа"])
    if not df.empty:
        df = df.sort_values(["ФИО", "_sort"])
    return df.drop(columns="_sort").reset_index(drop=True)


def _gia_matrix_header(c: str, members: dict) -> str:
    lst = members.get(c, [])
    return f"{c} ({', '.join(_gia_short(m) for m in lst)})" if lst else c


def _gia_matrix(sess: pd.DataFrame, members: dict, p: dict) -> pd.DataFrame:
    comms = list(members.keys())
    d0, d1 = date.fromisoformat(p["start"]), date.fromisoformat(p["end"])
    intervals = [(r, *_gia_interval(r)) for _, r in _gia_dated(sess).iterrows()]
    busy_days = {s.date() for _, s, _ in intervals}
    if busy_days and p["only_busy_days"]:
        d0, d1 = min(d0, min(busy_days)), max(d1, max(busy_days))
    index, data = [], []
    d = d0
    while d <= d1:
        if (p["weekends"] or d.weekday() < 5 or d in busy_days) and (not p["only_busy_days"] or d in busy_days):
            t = datetime.combine(d, dtime(p["hour_from"], 0))
            t_end = datetime.combine(d, dtime(23, 59)) if p["hour_to"] >= 24 else datetime.combine(d, dtime(p["hour_to"], 0))
            while t < t_end:
                slot_end = t + timedelta(minutes=p["step"])
                active = [(r, s, e) for r, s, e in intervals if s < slot_end and t < e]
                row = []
                for c in comms:
                    own = [(r, s, e) for r, s, e in active if r["Комиссия"] == c]
                    notes = []
                    for r, s, e in active:
                        if r["Комиссия"] == c:
                            continue
                        shared = set(members.get(c, [])) & set(members.get(r["Комиссия"], []))
                        for person in sorted(shared):
                            g = f"гр. {r['Группа']}, " if r["Группа"] else ""
                            notes.append(f"{_gia_short(person)} занят(а): {g}"
                                         f"{s.strftime('%H:%M')}–{e.strftime('%H:%M')}, {r['Комиссия']}")
                    if own:
                        r, s, e = own[0]
                        g = f"гр. {r['Группа']} " if r["Группа"] else ""
                        mark = g + f"{s.strftime('%H:%M')}–{e.strftime('%H:%M')}"
                        if len(own) > 1:
                            row.append("🟥 два заседания одной ГЭК: " + "; ".join(
                                (f"гр. {x['Группа']} " if x["Группа"] else "") + f"{a.strftime('%H:%M')}–{b.strftime('%H:%M')}"
                                for x, a, b in own))
                        elif notes:
                            row.append("🟥 " + mark + " – ПЕРЕСЕЧЕНИЕ: " + "; ".join(notes))
                        else:
                            row.append("🟦 " + mark)
                    else:
                        row.append("⛔ " + "; ".join(notes) if notes else "")
                index.append(f"{GIA_RU_WD[d.weekday()]} {t.strftime('%d.%m %H:%M')}")
                data.append(row)
                t = slot_end
        d += timedelta(days=1)
    return pd.DataFrame(data, index=pd.Index(index, name="Дата и время"),
                        columns=[_gia_matrix_header(c, members) for c in comms])


def _gia_excel_bytes() -> bytes:
    comm, sess, p = st.session_state.gia_comm, st.session_state.gia_sess, st.session_state.gia_params
    members = _gia_members()
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        # служебные листы – по ним проект восстанавливается
        comm.to_excel(w, sheet_name="Комиссии", index=False)
        sess.to_excel(w, sheet_name="Заседания", index=False)
        _gia_params_df(p).to_excel(w, sheet_name="Параметры", index=False)
        # листы для работы и рассылки
        _gia_summary(sess, members).to_excel(w, sheet_name="Итог", index=False)
        _gia_by_person(sess, members).to_excel(w, sheet_name="По членам комиссий", index=False)
        if members:
            _gia_matrix(sess, members, p).to_excel(w, sheet_name="Матрица")
    return out.getvalue()


# ---------------------------------------------------------------------
# Хранение: Google Таблица (если настроена) + локальный файл + Excel
# ---------------------------------------------------------------------
def _gia_gs_enabled() -> bool:
    try:
        return "gcp_service_account" in st.secrets and "sheet_url" in st.secrets.get("gia", {})
    except Exception:
        return False


@st.cache_resource(show_spinner=False)
def _gia_gs_book():
    import gspread
    gc = gspread.service_account_from_dict(dict(st.secrets["gcp_service_account"]))
    return gc.open_by_url(st.secrets["gia"]["sheet_url"])


def _gia_gs_write(book, title: str, df: pd.DataFrame):
    try:
        ws = book.worksheet(title)
    except Exception:
        ws = book.add_worksheet(title=title, rows=200, cols=max(len(df.columns), 2))
    values = [list(df.columns)] + df.astype(str).values.tolist()
    if ws.row_count < len(values) + 1:
        ws.add_rows(len(values) + 1 - ws.row_count)
    # сначала пишем новые данные, потом чистим хвост — так данные не теряются при сбое
    ws.update(range_name="A1", values=values, value_input_option="RAW")
    last = max(ws.row_count, len(values) + 1)
    ws.batch_clear([f"A{len(values) + 1}:Z{last}"])


def _gia_gs_read(book, title: str) -> pd.DataFrame | None:
    try:
        ws = book.worksheet(title)
    except Exception:
        return None
    rows = ws.get_all_values()
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows[1:], columns=rows[0])


def _gia_params_df(p: dict) -> pd.DataFrame:
    return pd.DataFrame({"Параметр": list(p.keys()), "Значение": [str(v) for v in p.values()]})


def _gia_params_from_df(df: pd.DataFrame | None) -> dict:
    if df is None or df.empty or "Параметр" not in df.columns:
        return {}
    return dict(zip(df["Параметр"].astype(str), df["Значение"].astype(str)))


def _gia_persist():
    """Сохраняет ВСЁ сразу после каждого изменения."""
    comm, sess, p = st.session_state.gia_comm, st.session_state.gia_sess, st.session_state.gia_params
    now = datetime.now().strftime("%H:%M:%S")
    msgs = []
    # 1) локальный файл (атомарная запись: сначала во временный, потом замена)
    try:
        payload = {"commissions": comm.to_dict("records"), "sessions": sess.to_dict("records"), "params": p}
        tmp = GIA_LOCAL_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, GIA_LOCAL_FILE)
    except Exception as e:
        msgs.append(f"локальная копия не записалась ({e})")
    # 2) Google Таблица
    if _gia_gs_enabled():
        try:
            book = _gia_gs_book()
            _gia_gs_write(book, "Комиссии", comm)
            _gia_gs_write(book, "Заседания", sess)
            _gia_gs_write(book, "Параметры", _gia_params_df(p))
            st.session_state.gia_status = ("ok", f"✅ Сохранено в Google Таблицу в {now}")
        except Exception as e:
            st.session_state.gia_status = (
                "err", f"⚠️ Google Таблица недоступна ({e}). Данные сохранены в локальной копии, "
                       f"на всякий случай скачайте файл проекта."
            )
    else:
        st.session_state.gia_status = (
            "warn", f"💾 Сохранено в локальной копии в {now}. Google Таблица не подключена — "
                    f"после перезапуска приложения данные восстановятся только из файла проекта."
        )
    if msgs:
        st.session_state.gia_status = ("err", "⚠️ " + "; ".join(msgs) + ". Скачайте файл проекта.")


def _gia_load():
    """Загрузка при открытии: Google Таблица -> локальный файл -> пусто."""
    comm = sess = None
    params = {}
    source = "пустой проект"
    if _gia_gs_enabled():
        try:
            book = _gia_gs_book()
            comm = _gia_gs_read(book, "Комиссии")
            sess = _gia_gs_read(book, "Заседания")
            params = _gia_params_from_df(_gia_gs_read(book, "Параметры"))
            source = "Google Таблица"
        except Exception as e:
            st.session_state.gia_status = ("err", f"⚠️ Не удалось прочитать Google Таблицу ({e}). Открыта локальная копия.")
            comm = sess = None
    if comm is None and os.path.exists(GIA_LOCAL_FILE):
        try:
            with open(GIA_LOCAL_FILE, encoding="utf-8") as fh:
                data = json.load(fh)
            comm = pd.DataFrame(data.get("commissions", []))
            sess = pd.DataFrame(data.get("sessions", []))
            params = data.get("params", {})
            source = "локальная копия"
        except Exception:
            pass
    c, s, p = _gia_normalize(comm, sess, params)
    st.session_state.gia_comm, st.session_state.gia_sess, st.session_state.gia_params = c, s, p
    st.session_state.setdefault("gia_status", ("info", f"Открыто: {source}"))


def _gia_commit(flash: str | None = None):
    """Нормализовать, сохранить, обновить виджеты."""
    c, s, p = _gia_normalize(st.session_state.gia_comm, st.session_state.gia_sess, st.session_state.gia_params)
    st.session_state.gia_comm, st.session_state.gia_sess, st.session_state.gia_params = c, s, p
    _gia_persist()
    st.session_state.gia_ver += 1
    if flash:
        st.session_state.gia_flash = flash


def _gia_import_excel(file) -> list[str]:
    """Возвращает список ошибок; пустой список = проект восстановлен."""
    try:
        sheets = pd.read_excel(file, sheet_name=None, dtype=str)
    except Exception as e:
        return [f"Не удалось прочитать файл: {e}"]
    errors = []
    for name in ("Комиссии", "Заседания"):
        if name not in sheets:
            errors.append(f"В файле нет листа «{name}».")
    if errors:
        return errors
    comm, sess = sheets["Комиссии"].fillna(""), sheets["Заседания"].fillna("")
    for c in GIA_COMM_COLS:
        if c not in comm.columns:
            errors.append(f"На листе «Комиссии» нет столбца «{c}».")
    for c in ["Комиссия", "Дата", "Начало", "Длительность, мин"]:
        if c not in sess.columns:
            errors.append(f"На листе «Заседания» нет столбца «{c}».")
    if errors:
        return errors
    c, s, p = _gia_normalize(comm, sess, _gia_params_from_df(sheets.get("Параметры")))
    skipped = len(sess[sess["Комиссия"].astype(str).str.strip() != ""]) - len(s)
    st.session_state.gia_comm, st.session_state.gia_sess, st.session_state.gia_params = c, s, p
    _gia_commit(f"✅ Проект восстановлен: {c['Комиссия'].nunique()} комиссий, {int((s["Дата"] != "").sum())} заседаний с датой"
                + (f" (пропущено строк с ошибкой в дате/времени: {skipped})" if skipped > 0 else ""))
    return []


# ---------------------------------------------------------------------
# Интерфейс вкладки
# ---------------------------------------------------------------------
GIA_TEXT_HELP = """ГЭК 1:
Группа: в3743801/41401
Председатель 1
Иванов Иван Иванович
Петрова Мария Сергеевна

ГЭК 2:
Группа: з3743801/40401
Председатель 2
Иванов Иван Иванович"""


def _gia_color(v):
    v = str(v)
    if v.startswith("🟥"):
        return "background-color:#f8d7da"
    if v.startswith("🟦"):
        return "background-color:#dbe9ff"
    if v.startswith("⛔"):
        return "background-color:#fff3cd"
    return ""


def render_gia_tab():
    st.subheader("⚖️ Планирование ГИА (защиты ВКР)")

    if "gia_comm" not in st.session_state:
        st.session_state.gia_ver = 0
        _gia_load()

    ver = st.session_state.gia_ver
    kind, text = st.session_state.get("gia_status", ("info", ""))
    {"ok": st.success, "warn": st.info, "err": st.error}.get(kind, st.caption)(text)
    if st.session_state.get("gia_flash"):
        st.success(st.session_state.pop("gia_flash"))
    for w in st.session_state.pop("gia_flash_warn", []) or []:
        st.warning(w)

    comms = _gia_commissions()
    members = _gia_members()
    sess = st.session_state.gia_sess
    p = st.session_state.gia_params

    # ---------- 1. Составы комиссий: одно поле ----------
    with st.expander("👥 Составы комиссий", expanded=not comms):
        st.caption(
            "Вставьте все составы одним текстом. Каждая комиссия начинается со строки с двоеточием "
            "(«ГЭК 1:»), ниже – ФИО по одному в строке. Первый в списке – председатель. "
            "Строка «Группа: …» необязательна: группы можно вписать и потом, в таблице заседаний. "
            "Сохраняется само, как только вы щёлкнете мышью вне поля (или нажмёте Ctrl+Enter)."
        )
        tkey = f"gia_text_{ver}"
        st.text_area(
            "Составы ГЭК", value=_gia_text_from_data(), key=tkey, height=320,
            placeholder=GIA_TEXT_HELP, on_change=_gia_apply_text, args=(tkey,),
        )
        st.caption("Чтобы удалить комиссию, сотрите её блок из текста. Уже внесённые даты её заседаний "
                   "не удалятся сами – их можно убрать в таблице ниже.")
        if comms:
            st.button("✔️ Применить составы", key=f"gia_apply_{ver}",
                      on_click=_gia_apply_text, args=(tkey,))

    if not comms:
        st.info("Вставьте составы комиссий – после этого появятся таблица заседаний и матрица занятости.")
    else:
        # ---------- 2. Заседания: председатели и даты ----------
        st.markdown("#### 🗓 Заседания ГЭК: даты защит")
        st.caption(
            "Впишите дату, время начала и длительность напротив председателя – матрица ниже обновится сразу "
            "и покажет занятость этих людей во всех ГЭК. Если у ГЭК несколько дней защит, добавьте строку "
            "внизу таблицы (знак «+») и выберите ГЭК. Удалить строку: отметьте её слева и нажмите значок корзины."
        )
        orphan = sess[~sess["Комиссия"].isin(comms)]
        if not orphan.empty:
            st.warning("Есть заседания комиссий, которых больше нет в составах: "
                       + ", ".join(sorted(orphan["Комиссия"].unique())))
            if st.button("🗑 Удалить эти заседания", key=f"gia_orph_{ver}"):
                st.session_state.gia_sess = sess[sess["Комиссия"].isin(comms)]
                _gia_commit("Заседания удалённых комиссий убраны")
                st.rerun()

        conf_all = _gia_all_conflicts(sess, members)

        def _end(r):
            return _gia_interval(r)[1].strftime("%H:%M") if r["Дата"] else ""

        view = pd.DataFrame({
            "ID": sess["ID"].values,
            "ГЭК": sess["Комиссия"].values,
            "Председатель": [_gia_chair(members, c) for c in sess["Комиссия"]],
            "Группа": sess["Группа"].values,
            "Дата": [date.fromisoformat(d) if d else None for d in sess["Дата"]],
            "Начало": [_gia_parse_time(t) for t in sess["Начало"]],
            "Длительность, мин": sess["Длительность, мин"].astype(int).values,
            "Окончание": [_end(r) for _, r in sess.iterrows()],
            "Пересечения": ["⚠️ " + "; ".join(conf_all[i]) if conf_all.get(i) else ("✅ нет" if d else "")
                            for i, d in zip(sess["ID"], sess["Дата"])],
        })
        edited = st.data_editor(
            view, key=f"gia_sess_editor_{ver}", hide_index=True, width="stretch", num_rows="dynamic",
            column_config={
                "ID": None,
                "ГЭК": st.column_config.SelectboxColumn("ГЭК", options=comms, required=True),
                "Председатель": st.column_config.TextColumn("Председатель", disabled=True),
                "Группа": st.column_config.TextColumn("Группа"),
                "Дата": st.column_config.DateColumn("Дата", format="DD.MM.YYYY"),
                "Начало": st.column_config.TimeColumn("Начало", format="HH:mm", step=60 * 30),
                "Длительность, мин": st.column_config.NumberColumn("Длительность, мин", min_value=30,
                                                                   max_value=600, step=30),
                "Окончание": st.column_config.TextColumn("Окончание", disabled=True),
                "Пересечения": st.column_config.TextColumn("Пересечения", disabled=True, width="large"),
            },
        )
        known = set(sess["ID"])
        new_rows = []
        for _, r in edited.iterrows():
            rid = str(r["ID"]) if (not pd.isna(r["ID"]) and str(r["ID"]) in known) else uuid.uuid4().hex[:8]
            d, t = r["Дата"], r["Начало"]
            if isinstance(d, (pd.Timestamp, datetime)):
                d = d.date()
            new_rows.append({
                "ID": rid,
                "Комиссия": "" if pd.isna(r["ГЭК"]) else str(r["ГЭК"]),
                "Дата": d.isoformat() if isinstance(d, date) else "",
                "Начало": t.strftime("%H:%M") if isinstance(t, dtime) else GIA_DEFAULT_START,
                "Длительность, мин": GIA_DEFAULT_DUR if pd.isna(r["Длительность, мин"]) else int(r["Длительность, мин"]),
                "Группа": "" if pd.isna(r["Группа"]) else str(r["Группа"]),
            })
        _, new_sess, _ = _gia_normalize(st.session_state.gia_comm, pd.DataFrame(new_rows, columns=GIA_SESS_COLS), p)
        if not new_sess.astype(str).reset_index(drop=True).equals(sess[GIA_SESS_COLS].astype(str).reset_index(drop=True)):
            st.session_state.gia_sess = new_sess
            _gia_commit("✅ Даты сохранены")
            st.rerun()

        n_conf = sum(1 for v in conf_all.values() if v)
        if n_conf:
            st.error(f"Заседаний с пересечениями: {n_conf}. Подробности – в столбце «Пересечения» и в матрице (🟥).")

        # ---------- 3. Матрица занятости (всегда открыта) ----------
        st.markdown("#### 🧮 Матрица занятости")
        with st.expander("⚙️ Настройки матрицы", expanded=False):
            m1, m2, m3, m4 = st.columns(4)
            ms = m1.date_input("С", date.fromisoformat(p["start"]), format="DD.MM.YYYY", key=f"gia_ms_{ver}")
            me = m2.date_input("По", date.fromisoformat(p["end"]), format="DD.MM.YYYY", key=f"gia_me_{ver}")
            hf, ht = m3.slider("Часы", 6, 23, (p["hour_from"], p["hour_to"]), key=f"gia_h_{ver}")
            step = m4.selectbox("Шаг", [30, 60], index=[30, 60].index(p["step"]) if p["step"] in (30, 60) else 0,
                                format_func=_gia_dur_label, key=f"gia_step_{ver}")
            o1, o2 = st.columns(2)
            wk = o1.checkbox("Показывать выходные", p["weekends"], key=f"gia_wk_{ver}")
            obd = o2.checkbox("Только дни, где есть защиты", p["only_busy_days"], key=f"gia_obd_{ver}")
            new_p = {"start": ms.isoformat(), "end": me.isoformat(), "hour_from": hf, "hour_to": ht,
                     "step": step, "weekends": wk, "only_busy_days": obd}
            if new_p != {k: p[k] for k in new_p}:
                st.session_state.gia_params = {**p, **new_p}
                _gia_commit()
                st.rerun()
        st.caption("🟦 заседание ГЭК (группа и время) · ⛔ член этой ГЭК в это время занят в другой · "
                   "🟥 пересечение: у ГЭК заседание, а её член занят в другой, или два заседания одной ГЭК")
        mx = _gia_matrix(sess, members, p)
        if _gia_dated(sess).empty:
            st.info("Матрица заполнится, когда в таблице заседаний появится хотя бы одна дата.")
            st.dataframe(pd.DataFrame(columns=[_gia_matrix_header(c, members) for c in comms]),
                         hide_index=True, width="stretch")
        elif mx.empty:
            st.caption("В выбранном периоде нет слотов для показа – проверьте настройки матрицы.")
        else:
            sty = mx.style.map(_gia_color) if hasattr(mx.style, "map") else mx.style.applymap(_gia_color)
            st.dataframe(sty, width="stretch", height=min(40 + 35 * len(mx), 700))

        # ---------- 4. По членам комиссий ----------
        with st.expander("👤 Расписание по членам комиссий", expanded=False):
            bp = _gia_by_person(sess, members)
            if bp.empty:
                st.caption("Нет данных.")
            else:
                who = st.selectbox("Член комиссии", ["Все"] + sorted(bp["ФИО"].unique()), key=f"gia_who_{ver}")
                st.dataframe(bp if who == "Все" else bp[bp["ФИО"] == who], hide_index=True, width="stretch")

    # ---------- 5. Файл проекта ----------
    st.markdown("#### 💾 Файл проекта")
    e1, e2 = st.columns(2)
    with e1:
        st.download_button(
            "📥 Скачать проект (Excel)", data=_gia_excel_bytes(),
            file_name=f"ГИА_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="stretch", key=f"gia_dl_{ver}",
        )
        st.caption("В файле: составы, заседания, итог «ФИО – дата – время – группа», расписание по людям и матрица.")
    with e2:
        up = st.file_uploader("📂 Восстановить из файла проекта (.xlsx)", type=["xlsx"], key=f"gia_up_{ver}")
        if up is not None:
            st.warning("Текущие данные будут заменены данными из файла.")
            if st.button("Восстановить", type="primary", width="stretch", key=f"gia_up_btn_{ver}"):
                errs = _gia_import_excel(up)
                if errs:
                    for e in errs:
                        st.error(e)
                else:
                    st.rerun()
# ======================= КОНЕЦ БЛОКА ГИА =======================


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📥 Вывод расписания",
  "🔍 Поиск свободных окон",
    "📊 Статистика",
     "⚖️ Планирование ГИА",
    "📥 Выгрузка всего и сразу (тест)"
])

with tab2:
    st.subheader("🔍 Свободные окна")
    st.markdown(
        "Находит временные промежутки между занятиями, в которые можно поставить или перенести пару."
    )

    col_g, col_t = st.columns(2)
    with col_g:
        win_groups = st.multiselect("Группы", options=sorted(GROUP_MAP.keys()), key="win_groups")
    with col_t:
        win_teachers = st.multiselect("Преподаватели", options=sorted(TEACHER_MAP.keys()), key="win_teachers")

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        win_start = st.date_input("Начало периода", datetime(2026, 2, 1).date(), key="win_start")
    with col_d2:
        win_end = st.date_input("Конец периода", datetime(2026, 5, 25).date(), key="win_end")

    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
    with col_cfg1:
        duration_options = {"30 мин": 30, "45 мин": 45, "1 час": 60, "1.5 часа": 90, "2 часа": 120}
        dur_label = st.selectbox("Мин. длительность окна", list(duration_options.keys()), key="win_dur")
        min_duration_val = duration_options[dur_label]
    with col_cfg2:
        win_weekdays = st.checkbox("Только будни", value=True, key="win_weekdays")
    with col_cfg3:
        win_mode = st.radio("Режим поиска", ["Все свободны", "Минимум N из M"], horizontal=True, key="win_mode")

    all_win_participants = win_groups + win_teachers

    if win_mode == "Минимум N из M":
        max_n = max(len(all_win_participants), 1)
        default_n = max(1, len(all_win_participants) - 1)
        win_min_free = st.number_input(
            "Минимум свободных участников (N)",
            min_value=1, max_value=max_n, value=default_n, step=1, key="win_n"
        )
    else:
        win_min_free = len(all_win_participants)

    win_required = st.multiselect(
        "Обязательные участники (всегда должны быть свободны)",
        options=all_win_participants,
        key="win_required"
    )

    if st.button("🔎 Найти свободные окна", type="primary", key="win_search"):
        if not win_groups and not win_teachers:
            st.warning("Выберите хотя бы одну группу или преподавателя")
        elif win_start > win_end:
            st.warning("Дата начала не может быть позже даты окончания")
        else:
            with st.spinner("Загрузка расписаний..."):
                all_schedules = {}
                total = len(win_groups) + len(win_teachers)
                progress = st.progress(0, text="0%") if total > 0 else None
                done = 0

                for g in win_groups:
                    try:
                        df = parse_group_schedule(g, win_start, win_end, show_progress=False)
                        all_schedules[g] = add_parsed_date(df)
                    except Exception as e:
                        st.warning(f"Ошибка загрузки группы {g}: {e}")
                        all_schedules[g] = pd.DataFrame()
                    done += 1
                    if progress:
                        progress.progress(done / total, text=f"{int(done / total * 100)}%")

                for t in win_teachers:
                    try:
                        df = parse_teacher_schedule(t, win_start, win_end, show_progress=False)
                        all_schedules[t] = add_parsed_date(df)
                    except Exception as e:
                        st.warning(f"Ошибка загрузки преподавателя {t}: {e}")
                        all_schedules[t] = pd.DataFrame()
                    done += 1
                    if progress:
                        progress.progress(done / total, text=f"{int(done / total * 100)}%")

                if progress:
                    progress.empty()

            with st.spinner("Поиск окон..."):
                min_duration_td = timedelta(minutes=min_duration_val)
                mode_code = "hard" if win_mode == "Все свободны" else "soft"
                windows = find_common_free_windows(
                    all_schedules,
                    all_win_participants,
                    win_start,
                    win_end,
                    min_duration_td,
                    win_weekdays,
                    mode_code,
                    win_min_free,
                    set(win_required)
                )

            if not windows:
                st.info("Свободных окон, удовлетворяющих условиям, не найдено.")
            else:
                st.success(f"Найдено {len(windows)} свободных окон")

                from collections import defaultdict
                by_day = defaultdict(list)
                for w in windows:
                    by_day[w['date']].append(w)

                export_rows = []
                weekday_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

                for day, day_windows in sorted(by_day.items()):
                    day_str = day.strftime("%d.%m.%Y")
                    wday = weekday_names[day.weekday()]
                    expander_label = f"📅 {day_str} ({wday}) — {len(day_windows)} окон"

                    with st.expander(expander_label, expanded=(len(by_day) <= 3)):
                        for w in day_windows:
                            nice_s = w['nice_start'].strftime("%H:%M")
                            nice_e = w['nice_end'].strftime("%H:%M")
                            real_s = w['real_start'].strftime("%H:%M")
                            real_e = w['real_end'].strftime("%H:%M")

                            if w['free_count'] == w['total_count']:
                                icon = "🟢"
                                status_text = f"Свободны: все ({w['total_count']} из {w['total_count']})"
                            else:
                                icon = "🟡"
                                status_text = f"Свободны: {w['free_count']} из {w['total_count']}"

                            st.markdown(f"**{icon} Окно {nice_s} – {nice_e}**")
                            st.caption(f"Реальный промежуток: {real_s} – {real_e}")
                            st.write(status_text)

                            if w['busy_participants']:
                                busy_details = []
                                for bp in w['busy_participants']:
                                    df_bp = all_schedules.get(bp)
                                    if df_bp is not None and not df_bp.empty and 'Дата_parsed' in df_bp.columns:
                                        day_df = df_bp[df_bp['Дата_parsed'] == day]
                                        for _, row in day_df.iterrows():
                                            t_s, t_e = parse_lesson_time(row['Время'])
                                            if t_s and t_e:
                                                dt_s = datetime.combine(day, t_s)
                                                dt_e = datetime.combine(day, t_e)
                                                if dt_s < w['real_end'] and dt_e > w['real_start']:
                                                    subject = row['Дисциплина']
                                                    place = row.get('Место', 'Не указано')
                                                    if 'Группа' in row and pd.notna(row['Группа']) and str(row['Группа']).strip():
                                                        teacher = row.get('Преподаватель', 'Не указано')
                                                        busy_details.append(f"**{bp}**: {row['Время']} {subject} ({teacher}) · {place}")
                                                    else:
                                                        groups = row.get('Группы', 'Не указано')
                                                        busy_details.append(f"**{bp}**: {row['Время']} {subject} (гр. {groups}) · {place}")
                                                    break
                                if busy_details:
                                    st.write("**Заняты:**")
                                    for bd in busy_details:
                                        st.write(f"- {bd}")

                            # Таблица контекста
                            ctx_rows = []
                            for p in all_win_participants:
                                df_p = all_schedules.get(p)
                                before = get_lesson_context(df_p, day, w['real_start'], 'before')
                                after = get_lesson_context(df_p, day, w['real_end'], 'after')
                                label = f"Группа {p}" if p in win_groups else f"Преподаватель {p}"
                                ctx_rows.append({"Участник": label, "До окна": before, "После окна": after})

                            st.dataframe(pd.DataFrame(ctx_rows), use_container_width=True, hide_index=True)
                            st.divider()

                            export_rows.append({
                                "Дата": day_str,
                                "День недели": wday,
                                "Удобное начало": nice_s,
                                "Удобное окончание": nice_e,
                                "Реальное начало": real_s,
                                "Реальное окончание": real_e,
                                "Свободных": w['free_count'],
                                "Всего участников": w['total_count'],
                                "Статус": "Все свободны" if w['free_count'] == w['total_count'] else f"{w['free_count']} из {w['total_count']}",
                                "Заняты": ", ".join(w['busy_participants']) if w['busy_participants'] else ""
                            })

                if export_rows:
                    exp_df = pd.DataFrame(export_rows)
                    out = io.BytesIO()
                    with pd.ExcelWriter(out, engine="openpyxl") as writer:
                        exp_df.to_excel(writer, sheet_name="Свободные окна", index=False)
                    st.download_button(
                        label="📥 Экспорт найденных окон в Excel",
                        data=out.getvalue(),
                        file_name=f"free_windows_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

with tab1:
    st.subheader("📥 Вывод расписания")
    mode = st.radio("Что выводим?", ["Расписание группы", "Расписание преподавателя"], horizontal=True)
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Дата начала", datetime(2026, 2, 1))
    with col2:
        end_date = st.date_input("Дата окончания", datetime(2026, 5, 25))

    if mode == "Расписание группы":
        group_human = st.selectbox("Выберите группу", list(GROUP_MAP.keys()))
        if st.button("Показать расписание группы", type="primary"):
            with st.spinner("Парсинг..."):
                df = parse_group_schedule(group_human, start_date, end_date)
                if not df.empty:
                    st.session_state.schedule_data = {f"Группа {group_human}": df}
                    st.success(f"✅ Загружено {len(df)} занятий")
                    display_schedule_by_date(df, f"Группа {group_human}")
    else:
        teacher_name = st.selectbox("Выберите преподавателя", list(TEACHER_MAP.keys()))
        if st.button("Показать расписание преподавателя", type="primary"):
            with st.spinner("Парсинг..."):
                df = parse_teacher_schedule(teacher_name, start_date, end_date)
                if not df.empty:
                    st.session_state.schedule_data = {f"Преподаватель {teacher_name}": df}
                    st.success(f"✅ Загружено {len(df)} занятий")
                    display_schedule_by_date(df, f"Преподаватель {teacher_name}")

 
    if 'schedule_data' in st.session_state and st.session_state.schedule_data:
        st.markdown("---")
        st.subheader("Загруженные данные")
        for key, df in st.session_state.schedule_data.items():
            display_schedule_by_date(df, key)



with tab3:
    st.subheader("📊 Статистика")
    if 'schedule_data' in st.session_state and st.session_state.schedule_data:
        entities = list(st.session_state.schedule_data.keys())
        st.write("**Расписания загружены для:** " + ", ".join(entities))
        all_dfs = list(st.session_state.schedule_data.values())
        combined = pd.concat(all_dfs, ignore_index=True)
        st.metric("Всего занятий", len(combined))
        st.metric("Период", f"{combined['Дата'].min()} — {combined['Дата'].max()}")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**По типам занятий:**")
            st.dataframe(combined['Тип занятия'].value_counts())
        with col2:
            st.write("**По преподавателям:**")
            st.dataframe(combined['Преподаватель'].value_counts())

     
        export_df = prepare_export_dataframe(combined)
        if not export_df.empty:
            output = io.BytesIO()
            with pd.ExcelWriter(output) as writer:
            
                export_df.to_excel(writer, sheet_name='Отчет', index=False)
            excel_data = output.getvalue()
            st.download_button(
                label="📥 Выгрузить Excel",
                data=excel_data,
                file_name=f"statistics_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
     
    else:
        st.info("Загрузите расписание на вкладке 'Вывод расписания'")
        


# with tab2:
#     st.subheader("🔍 Поиск свободных окон")
#     st.write("**Выберите группы и преподавателей:**")
#     selected_groups = st.multiselect("Группы", options=list(GROUP_MAP.keys()))
#     selected_teachers = st.multiselect("Преподаватели", options=list(TEACHER_MAP.keys()))
#     col1, col2 = st.columns(2)
#     with col1:
#         search_start = st.date_input("Начало периода", datetime(2026, 2, 1), key="search_start")
#     with col2:
#         search_end = st.date_input("Конец периода", datetime(2026, 2, 28), key="search_end")
#     duration_options = {"30 минут": 30, "1 час": 60, "1.5 часа": 90, "2 часа": 120}
#     min_duration_label = st.selectbox("Мин. длительность окна", list(duration_options.keys()))
#     min_duration = duration_options[min_duration_label]
# 
#     if st.button("🔎 Построить общее расписание", type="primary"):
#         if not selected_groups and not selected_teachers:
#             st.warning("Выберите хотя бы одну группу или преподавателя")
#         else:
#             with st.spinner("Загрузка расписаний..."):
#                 schedule_dfs = []
#                 if selected_groups:
#                     for g in selected_groups:
#                         df = parse_group_schedule(g, search_start, search_end)
#                         if not df.empty:
#                             schedule_dfs.append(df)
#                 if selected_teachers:
#                     for t in selected_teachers:
#                         df = parse_teacher_schedule(t, search_start, search_end)
#                         if not df.empty:
#                             schedule_dfs.append(df)
#                 if schedule_dfs:
#                     combined = pd.concat(schedule_dfs, ignore_index=True)
#                     st.success(f"Загружено расписание для {len(selected_groups)} групп и {len(selected_teachers)} преподавателей")
#                     display_schedule_by_date(df, f"Группа {group_human}")
#                 else:
#                     st.warning("Не удалось загрузить данные")


with tab4:
    # Вся логика вкладки — в функции render_gia_tab() (блок «ПЛАНИРОВАНИЕ ГИА» выше)
    render_gia_tab()


with tab5:
    st.subheader("📥 Массовая выгрузка расписаний")
    st.markdown("Выберите **несколько групп** и/или **несколько преподавателей**. Данные будут собраны в один Excel-файл.")

    if "mass_result" not in st.session_state:
        st.session_state.mass_result = None
    if "mass_excel" not in st.session_state:
        st.session_state.mass_excel = None

    col_g, col_t = st.columns(2)
    with col_g:
        st.markdown("**Группы**")
        selected_groups = st.multiselect(
            "Отметьте группы",
            options=sorted(GROUP_MAP.keys()),
            default=st.session_state.get("mass_selected_groups", []),
            key="multi_groups",
        )
    with col_t:
        st.markdown("**Преподаватели**")
        selected_teachers = st.multiselect(
            "Отметьте преподавателей",
            options=sorted(TEACHER_MAP.keys()),
            default=st.session_state.get("mass_selected_teachers", []),
            key="multi_teachers",
        )

    col1, col2 = st.columns(2)
    with col1:
        multi_start = st.date_input("Дата начала", datetime(2026, 2, 1).date(), key="multi_start")
    with col2:
        multi_end = st.date_input("Дата окончания", datetime(2026, 5, 25).date(), key="multi_end")
    TIME_SLOT_OPTIONS = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
    selected_times = st.multiselect(
        "Время начала пар (опционально)",
        options=TIME_SLOT_OPTIONS,
        default=st.session_state.get("mass_selected_times", []),
        key="multi_times",
        help="Если выбрать время — в выгрузку попадут только занятия, начинающиеся в это время "
             "(и только преподаватели, у которых есть такие пары). Пустой список = все занятия.",
    )

  
    st.caption(
        f"Выбрано: {len(selected_groups)} групп, {len(selected_teachers)} преподавателей"
        + (f", фильтр по времени: {', '.join(selected_times)}" if selected_times else "")
    )

    if st.button("📥 Собрать Excel по выбранным", type="primary", use_container_width=True):
        if not selected_groups and not selected_teachers:
            st.warning("Выберите хотя бы одну группу или одного преподавателя")
        else:
            st.session_state.mass_selected_groups = selected_groups
            st.session_state.mass_selected_teachers = selected_teachers
            st.session_state.mass_selected_times = selected_times

            all_dfs = []
            total = max(len(selected_groups) + len(selected_teachers), 1)
            progress = st.progress(0, text="0%")
            status = st.empty()
            done = 0

            for g in selected_groups:
                status.info(f"Парсим группу: {g} ({done + 1}/{total}) …")
                try:
                    df = parse_group_schedule(g, multi_start, multi_end, show_progress=True)
                    if not df.empty:
                        all_dfs.append(df)
                        st.success(f"✅ {g}: {len(df)} занятий")
                    else:
                        st.warning(f"⚠️ {g}: нет данных за выбранный период")
                except Exception as e:
                    st.error(f"❌ Ошибка группы {g}: {e}")
                done += 1
                progress.progress(done / total, text=f"{int(done / total * 100)}%")

            for t in selected_teachers:
                status.info(f"Парсим преподавателя: {t} ({done + 1}/{total}) …")
                try:
                    df = parse_teacher_schedule(t, multi_start, multi_end, show_progress=True)
                    if not df.empty:
                        all_dfs.append(df)
                        st.success(f"✅ {t}: {len(df)} занятий")
                    else:
                        st.warning(f"⚠️ {t}: нет данных за выбранный период")
                except Exception as e:
                    st.error(f"❌ Ошибка преподавателя {t}: {e}")
                done += 1
                progress.progress(done / total, text=f"{int(done / total * 100)}%")

            status.empty()
            progress.progress(1.0, text="100%")

            if all_dfs:
                combined = pd.concat(all_dfs, ignore_index=True)

                # Фильтр по выбранному времени начала пары
                if selected_times:
                    def _matches_time(time_str):
                        t_start, _ = parse_lesson_time(time_str)
                        if t_start is None:
                            return False
                        return t_start.strftime("%H:%M") in selected_times

                    before = len(combined)
                    combined = combined[combined["Время"].apply(_matches_time)].copy()
                    st.info(
                        f"Фильтр по времени {', '.join(selected_times)}: "
                        f"оставлено {len(combined)} из {before} занятий"
                    )

                if combined.empty:
                    st.session_state.mass_result = None
                    st.session_state.mass_excel = None
                    st.warning("После фильтра по времени не осталось ни одного занятия")
                else:
                    st.session_state.mass_result = combined
                    st.session_state.schedule_data = {
                        f"Массовая выгрузка ({len(selected_groups)} гр. + {len(selected_teachers)} преп.)": combined
                    }

                    groups_sheet, teachers_sheet = prepare_sorted_raw_sheets(
                        combined,
                        selected_groups=selected_groups,
                        selected_teachers=selected_teachers,
                    )
                    summary_df = build_summary_report(
                        combined,
                        selected_groups=selected_groups,
                        selected_teachers=selected_teachers,
                        start_date=multi_start,
                        end_date=multi_end,
                    )
                    export_df = prepare_export_dataframe(combined)

                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        if not groups_sheet.empty:
                            groups_sheet.to_excel(writer, sheet_name="Группы", index=False)
                        if not teachers_sheet.empty:
                            teachers_sheet.to_excel(writer, sheet_name="Преподаватели", index=False)
                        if not summary_df.empty:
                            summary_df.to_excel(writer, sheet_name="Отчет", index=False)
                        if not export_df.empty:
                            export_df.to_excel(writer, sheet_name="Сводка по дисциплинам", index=False)
                    st.session_state.mass_excel = output.getvalue()
                    st.success(f"✅ Всего собрано {len(combined)} занятий")
            else:
                st.session_state.mass_result = None
                st.session_state.mass_excel = None
                st.warning("Не удалось загрузить ни одного расписания")

   
    if st.session_state.mass_result is not None:
        combined = st.session_state.mass_result
        st.metric("Всего занятий", len(combined))

        col_a, col_b = st.columns(2)
        with col_a:
            st.write("**По типам занятий:**")
            st.dataframe(combined["Тип занятия"].value_counts())
        with col_b:
            st.write("**По преподавателям:**")
            st.dataframe(combined["Преподаватель"].value_counts())

        if st.session_state.mass_excel is not None:
            st.download_button(
                label="📥 Скачать Excel",
                data=st.session_state.mass_excel,
                file_name=f"mass_schedule_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key="mass_download_btn",
            )

        if st.button("🗑 Очистить результат", use_container_width=True):
            st.session_state.mass_result = None
            st.session_state.mass_excel = None
            st.rerun()

