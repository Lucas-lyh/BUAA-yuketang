from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os

from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


# 配置Edge浏览器，启用用户登录状态保存
service = Service(os.path.join(os.path.abspath("."), "msedgedriver.exe"))
options = Options()


# 创建用户数据目录，用于保存登录状态和浏览器配置
user_data_dir = os.path.join(os.path.abspath("."), "user_data")
need_login = True
# 如果没有user_data, 则不打开无头模式，登陆后退出。
if os.path.exists(user_data_dir):
    need_login = False
    options.add_argument("--headless")
os.makedirs(user_data_dir, exist_ok=True)

# 设置用户数据目录，这样浏览器会保存登录状态、Cookie等信息
options.add_argument(f"--user-data-dir={user_data_dir}")
# 禁用自动化控制特征，某些网站会检测这一点
options.add_argument("--disable-blink-features=AutomationControlled")

# 使用配置好的选项创建WebDriver实例
driver = webdriver.Edge(service=service, options=options)

# 加载本地HTML文件
driver.get(os.path.join(os.path.abspath("./"), "index.html"))
driver.implicitly_wait(3)

from tqdm import trange

import sys

if need_login:
    print("请在20秒内登录.")
    time.sleep(20)
    driver.quit()
    # 重启该脚本
    os.execv(sys.executable, ["python"] + sys.argv)

print("找到用户记录，开始无头处理")
print("10秒倒计时开始...")
# 给用户20秒时间导航至成绩单页面
for _ in trange(10):
    time.sleep(1)


def change_to_new_handle(old_handles):
    for window_handle in driver.window_handles:
        if window_handle not in old_handles:
            driver.switch_to.window(window_handle)
            break


def doing_course():
    print("正在处理课程...")
    base_window = driver.current_window_handle
    pre_window_list = driver.window_handles
    course_list = driver.find_elements(By.CLASS_NAME, "complete-td")

    for i, item in enumerate(course_list):
        if (
            "视频" in item.find_element(By.XPATH, "..").text.strip()
            and "已" not in item.text
        ):
            pre_window_list = driver.window_handles
            # 打开并转换到新页面
            driver.execute_script(
                'document.getElementsByClassName("unit-name-hover")[arguments[0]].click()',
                i,
            )
            time.sleep(1)
            change_to_new_handle(pre_window_list)

            print("switch to window:", driver.current_window_handle)
            time.sleep(10)
            video_box = driver.find_elements(By.CLASS_NAME, "video-box")
            if len(video_box) == 0:
                video_box = driver.find_elements(
                    By.CLASS_NAME, "media-controls-subtitle-box"
                )

            # 等待结束
            if len(video_box) > 0:
                print("video_box founded")
                video_box = video_box[0]
                done = False
                try:
                    title = driver.find_element(
                        By.CLASS_NAME,
                        "detail-node-title",
                    ).text.strip()
                except:
                    title = driver.find_elements(By.CLASS_NAME, "title")[0].text.strip()
                while not done:
                    while (
                        len(
                            driver.find_elements(
                                By.CLASS_NAME,
                                "progress-wrap",
                            )
                        )
                        == 0
                    ):
                        print("progress not found, refresh...")
                        driver.refresh()
                        time.sleep(5)
                    video_box = driver.find_elements(By.CLASS_NAME, "video-box")
                    if len(video_box) == 0:
                        video_box = driver.find_elements(
                            By.CLASS_NAME, "media-controls-subtitle-box"
                        )
                    video_box = video_box[0]
                    progress = driver.find_elements(
                        By.CLASS_NAME,
                        "progress-wrap",
                    )[0].text
                    done = done or (
                        "已完成" in progress.strip() or "100" in progress.strip()
                    )
                    is_dual = (
                        len(driver.find_elements(By.CLASS_NAME, "digital-human")) > 0
                    )
                    if is_dual:
                        start_element = driver.find_element(
                            By.CLASS_NAME,
                            "play-status-box",
                        )
                        # 选择start_element的第二个div
                        start_element = start_element.find_elements(By.TAG_NAME, "div")[
                            1
                        ]
                        start_element = start_element.find_element(By.TAG_NAME, "svg")
                    else:
                        start_element = driver.find_element(
                            By.CLASS_NAME,
                            "xt_video_bit_play_btn",
                        )
                    ## 检测可见性
                    if start_element.is_displayed():
                        print("start play...")
                        # 点击
                        ActionChains(driver).click(start_element).perform()
                        # 等待点击生效
                        time.sleep(1)

                    time.sleep(0.2)
                    if not is_dual:
                        speed_element = driver.find_element(
                            By.CLASS_NAME,
                            "xt_video_player_speed",
                        )

                    else:
                        speed_element = driver.find_element(
                            By.CLASS_NAME,
                            "rate-btn",
                        )
                    speed_text = speed_element.get_attribute("innerText")
                    if speed_text is None:
                        speed_text = ""
                    if "3" not in speed_text and "2" not in speed_text:
                        print("text is:", speed_text)
                        print("change speed to 3x/2x...")
                        if not is_dual:
                            driver.execute_script(
                                """
    const rate =  3;    
    let speedwrap = document.getElementsByTagName("xt-speedbutton")[0];
    let speedlist = document.getElementsByTagName("xt-speedlist")[0];
    let speedlistBtn = speedlist.firstElementChild.firstElementChild;
    speedlistBtn.setAttribute('data-speed', rate);
    speedlistBtn.setAttribute('keyt', rate + '.00');
    speedlistBtn.innerText = rate + '.00X';
    // 模拟点击
    let mousemove = document.createEvent("MouseEvent");
    mousemove.initMouseEvent("mousemove", true, true, window, 0, 10, 10, 10, 10, 0, 0, 0, 0, 0, null);
    speedwrap.dispatchEvent(mousemove);
    speedlistBtn.click();
                                """
                            )
                        else:
                            ActionChains(driver).move_to_element(video_box).perform()
                            time.sleep(0.2)
                            ActionChains(driver).move_to_element(
                                speed_element
                            ).perform()
                            time.sleep(0.2)
                            x2element = driver.find_element(
                                By.CLASS_NAME,
                                "rate-config-box",
                            ).find_elements(By.TAG_NAME, "div",)[0]
                            # change speed
                            ActionChains(driver).move_to_element(x2element).click(
                                x2element
                            ).perform()
                            time.sleep(0.2)
                    else:
                        print("speed is 2x, skip...")
                    # 停一会
                    time.sleep(2)
                    print(title, "|", progress)

            # 回到列表
            success_close = False
            while not success_close:
                try:
                    driver.close()
                    success_close = True
                except:
                    time.sleep(1)
            driver.switch_to.window(base_window)

        print(f"已完成 {i + 1} / {len(course_list)}")


main_window_url = "https://buaa.yuketang.cn/pro/courselist"
driver.get(main_window_url)
main_window_handles = driver.window_handles
time.sleep(5)
courses_element_list = driver.find_elements(By.CLASS_NAME, "el-card__body")
course_len = len(courses_element_list)
for course_element_index in range(course_len):
    courses_element_list = driver.find_elements(By.CLASS_NAME, "el-card__body")
    course_element = courses_element_list[course_element_index]
    print("doing course:", course_element.get_attribute("innerText"))
    course_element.click()
    time.sleep(5)
    ActionChains(driver).click(
        driver.find_element(By.XPATH, "//li[text()='成绩单']")
    ).perform()
    time.sleep(2)
    doing_course()
    time.sleep(2)
    driver.get(main_window_url)
    time.sleep(2)
