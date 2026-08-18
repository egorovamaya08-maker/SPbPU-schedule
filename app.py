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
  "3730105/60003": "44223"
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
    "Якоб Полина Александровна": "25675"
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
                              "Группа": group_human
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
                                "Место": place
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


    if "Группы" in df.columns and "Группа" not in df.columns:

        df["Группа"] = df["Группы"].str.split(r',\s*')
        df = df.explode("Группа")
    elif "Группа" not in df.columns:

        return pd.DataFrame()

  
 
    df["Тип занятия"] = df["Тип занятия"].str.strip()

    agg_dict = {
      #"Преподаватель": lambda x: ", ".join(sorted([str(n).strip() for n in set(x.dropna()) if str(n).strip() != "Не указано"])),
      #  "Преподаватель": lambda x: ", ".join(sorted(set(x.dropna()))),
        "Преподаватель": combine_teachers,
        "Место": lambda x: ", ".join(sorted(set(x.dropna()))),
        "Тип занятия": lambda x: x.value_counts().to_dict()  # временный словарь
    }
    grouped = df.groupby(["Группа", "Дисциплина"], as_index=False).agg(agg_dict)


    type_counts = grouped["Тип занятия"].apply(pd.Series).fillna(0).astype(int)

    grouped = grouped.drop(columns=["Тип занятия"])
   
    result = pd.concat([grouped, type_counts], axis=1)

   
    result.insert(2, "Контроль", "")

    preferred_type_order = [
          "Лекции",
          "Практика",
          "Практическое занятие",
          "Семинар",
          "Консультация",
          "Экзамен",
          "Зачёт",
          "Зачет",
      ]

  
    cols = result.columns.tolist()

    if "Преподаватель" in cols:
        cols.remove("Преподаватель")
    if "Место" in cols:
        cols.remove("Место")
   
    fixed = ["Группа", "Дисциплина", "Контроль"]
   # other_types = [c for c in cols if c not in fixed]
    other_types = []
      for t in preferred_type_order:
          if t in cols and t not in fixed:
              other_types.append(t)
      
      for c in cols:
          if c not in fixed and c not in other_types:
              other_types.append(c)
    
    final_cols = fixed + other_types + ["Преподаватель", "Место"]

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

tab1, tab3, tab4, tab5 = st.tabs([
    "📥 Вывод расписания",
    "📊 Статистика",
#   "🔍 Поиск свободных окон",
    "⚖️ Планирование ГИА",
    "📥 Выгрузка всего и сразу (тест)"
])


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
    st.subheader("⚖️ Планирование ГИА")
    

    if "commission_data" not in st.session_state:
        st.session_state.commission_data = None
    
    colA, colB = st.columns(2)
    with colA:
        matrix_start = st.date_input("Начало периода", datetime(2026, 4, 1).date(), key="m_start")
    with colB:
        matrix_end = st.date_input("Конец периода", datetime(2026, 4, 5).date(), key="m_end")
    

    if st.button("🔄 Перестроить матрицу") or st.session_state.commission_data is None:
        time_slots = generate_time_slots(matrix_start, matrix_end)
        st.session_state.commission_data = build_empty_matrix(time_slots, list(COMMISSION_MEMBERS.keys()))
        st.session_state.commission_matrix = auto_mark_conflicts(st.session_state.commission_data, COMMISSION_MEMBERS)
        st.rerun()
    

    column_config = {
        comm: st.column_config.TextColumn(
            format_header(COMMISSION_MEMBERS[comm]),
            default="",
            max_chars=50,
        )
        for comm in COMMISSION_MEMBERS.keys()
    }
    
    edited_df = st.data_editor(
        st.session_state.commission_matrix if st.session_state.commission_matrix is not None else pd.DataFrame(),
        use_container_width=True,
        num_rows="fixed",
        key="commission_editor_final",
        column_config=column_config,
        hide_index=False,
    )
    
    col_save, col_export, col_import = st.columns(3)
    
    with col_save:
        if st.button("💾 Сохранить", type="primary", use_container_width=True):
            # Очищаем от меток
            clean_data = edited_df.copy()
            for col in clean_data.columns:
                clean_data[col] = clean_data[col].apply(
                    lambda x: re.sub(r'^[🟢🔴]\s*', '', str(x)) if pd.notna(x) else x
                )
            
            st.session_state.commission_data = clean_data
            st.session_state.commission_matrix = auto_mark_conflicts(clean_data, COMMISSION_MEMBERS)
            st.success("✅ Сохранено")
            st.rerun()
    
    with col_export:
        if st.session_state.commission_data is not None:
            csv = st.session_state.commission_data.to_csv()
            st.download_button(
                label="📥 Скачать CSV",
                data=csv,
                file_name=f"commissions_{matrix_start}_{matrix_end}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col_import:
        uploaded = st.file_uploader("📂 Загрузить", type=['csv'], key="commission_upload")
        if uploaded is not None:
            df = pd.read_csv(uploaded, index_col=0)
            if set(df.columns) == set(COMMISSION_MEMBERS.keys()):
                st.session_state.commission_data = df
                st.session_state.commission_matrix = auto_mark_conflicts(df, COMMISSION_MEMBERS)
                st.success("✅ Загружено!")
                st.rerun()


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

    st.caption(f"Выбрано: {len(selected_groups)} групп, {len(selected_teachers)} преподавателей")

    if st.button("📥 Собрать Excel по выбранным", type="primary", use_container_width=True):
        if not selected_groups and not selected_teachers:
            st.warning("Выберите хотя бы одну группу или одного преподавателя")
        else:
            st.session_state.mass_selected_groups = selected_groups
            st.session_state.mass_selected_teachers = selected_teachers

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
