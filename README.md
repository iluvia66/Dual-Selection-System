# 双向选择系统
database design
## 业务概述
系统涉及三条任务线，总的来说：
- 第一条是关于遴选每年的研究生导师，并提供名额，招生指标、维护导师的个人信息；
- 第二条是关于考生，将通过复试的考生进行信息的存储维护、记录考生志愿即选择导师的过程；
- 第三条是关于志愿匹配的过程，分为两个阶段、第一个阶段，导师选择自己的志愿学生，统一选择完毕后，按照志愿优先的顺序，进行匹配的动作；匹配完毕后，进入自由匹配的阶段，将无学生选择的或者还有匹配名额的导师通过一定顺序选择未匹配导师的学生，每轮导师选择一个或者不选学生，五轮过后，若还有剩余学生则由管理员手动匹配。

## 分支管理
三条业务线分开开发，在flask+SQL server的框架下完成相关代码
### 业务线3的文件目录
```md
dual_select_system
│
├── app/
│   ├── __init__.py        # Flask 初始化文件
│   ├── routes/            # 存放路由文件
│   │   ├── candidate.py  
│   │   ├── advisor.py  
│   │   ├── preference.py 
│   │   └── task_line3.py  # 任务线3相关的路由
│   ├── models/            # 存放数据库模型
│   │   ├── candidate.py   # Candidate模型
│   │   ├── advisor.py     # Advisor模型
│   │   ├── preference.py  # Preference_Match模型
│   ├── dao/               # 持久层（Data Access Objects）
│   │   ├── candidate_dao.py
│   │   ├── advisor_dao.py
│   │   ├── preference_dao.py
│   └── utils/             # 工具函数
│       └── db_utils.py    # 数据库相关工具
│   └── templates/ 
│       └──advisor_candidates.html #前端页面 
│       └──admin_matching.html
│       └──error_page.html
│       └──admin_free_matching.html
│       └──free_matching.html
├── config.py              # Flask 配置文件
└── run.py                 # 启动应用的文件
```
