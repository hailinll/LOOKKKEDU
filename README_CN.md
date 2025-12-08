# LOOKKKEDU 18 社区版（中文快速指南）

本仓库是一组基于 Odoo 18 的教育场景插件，已统一品牌为 LOOKKKEDU，涵盖招生、学籍、课程/课表、考勤、考试、费用、图书馆、家长、活动、作业、教室/设施等，同时附带官网主题与完整的中文翻译。

## 目录与模块概览
- `openeducat_core`：核心数据与菜单（学生/教职工/课程/班级/学年学期/门户），学生证、在读证明等证件报表。
- `openeducat_activity`：课外活动/社团。
- `openeducat_admission`：招生申请、录取流程与分析报表。
- `openeducat_assignment`：作业布置与提交，含自动化规则。
- `openeducat_attendance`：考勤登记/报表，与课表联动。
- `openeducat_classroom`：教室与设施分配。
- `openeducat_exam`：考试、准考证、成绩单、成绩模板、考场编排。
- `openeducat_facility`：设施/设备管理。
- `openeducat_fees`：收费项目、学费条目、费用分析。
- `openeducat_library`：图书/媒体借阅、预约、条码与借阅卡。
- `openeducat_parent`：家长与亲属关系。
- `openeducat_timetable`：课表与时间段生成。
- `openeducat_erp`：整合安装包（一次安装主要功能）。
- `theme_web_openeducat`：网站/前端主题。
- 根目录：`README.md`（英文说明）、`LICENSE`（LGPL-3）、`cfg_run_flake8.cfg`/`cfg_run_pylint.cfg`（质量配置）。

## 快速运行（Docker 示例）
1) 准备 Postgres（示例：`postgres:15`），设置用户/密码/库名。  
2) 运行 Odoo 18，挂载本仓库为额外插件路径：
```bash
docker run -d --name educat-odoo --network <your-net> -p 8069:8069 \
  -v /Users/liuhailin/dev/educat:/mnt/extra-addons \
  -e HOST=<postgres-host> -e PORT=<5432> -e USER=<db-user> -e PASSWORD=<db-pass> \
  odoo:18 --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
```
3) 打开浏览器 `http://localhost:8069`，创建数据库后先安装 `openeducat_core`，再按需求安装其他模块，或直接安装整合包 `openeducat_erp`。

## 模块升级（加载最新翻译/改动）
在容器内执行（示例数据库名 `educat`，连接参数按实际替换）：
```bash
odoo --db_host=educat-db --db_port=5432 --db_user=odoo --db_password=odoo \
  -d educat -u openeducat_core,openeducat_library,openeducat_admission,openeducat_assignment,openeducat_attendance,openeducat_classroom,openeducat_exam,openeducat_facility,openeducat_fees,openeducat_parent,openeducat_timetable,openeducat_activity,openeducat_erp \
  --stop-after-init --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
```
仅刷新证件/图书馆相关可用：`-u openeducat_core,openeducat_library`。

## 主要报表/证件
- 学生证：`openeducat_core.report_student_idcard`
- 在读证明：`openeducat_core.report_student_bonafide`（中文模板，已安全处理空课程数据）
- 借阅卡：`openeducat_library.report_student_library_card`
打印文件名会自动拼接学生姓名，已修复全角符号导致的报表报错。

## 用户角色与权限
- 后台管理员 `openeducat_core.group_op_back_office_admin`：全量读写，含学生/教师/课程/课表/报表/证件。
- 教职工 `openeducat_core.group_op_faculty`：教学相关读写，部分模型只读或无删除。
- 家长管理员 `openeducat_parent.group_op_parent_manager`：管理家长与亲属关系（需安装家长模块）。
- 门户家长/学生（`base.group_portal` + 家长模块规则）：仅可访问与自身/子女相关数据，无后台管理权限。
入口：设置 > 用户和公司 > 用户，访问权限标签勾选；开发者模式下可在 设置 > 技术 > 安全 > 组 查看继承与域规则。

## 代码位置速览
- `__manifest__.py`：模块依赖、名称、描述。
- `security/*.xml`：访问控制与记录规则。
- `views/`：界面、动作、菜单。
- `report/`：QWeb 报表模板与报表动作。
- `static/`：JS/CSS/图片。
- `data/`：初始化数据、序列、参数。
- `demo/`：演示数据。
- `i18n/`：翻译文件（中文术语已统一：学生证/在读证明/借阅卡/学年/学期/学号/院系/教职工等）。

## 翻译与品牌
- 品牌已统一为 LOOKKKEDU，中文翻译按常用表述优化，避免全角符号导致报表错误。
- 若需自定义术语，可在 `i18n/zh_CN.po` 中追加/调整翻译后重新升级对应模块。

## 开发与调试提示
- 开启开发者模式后，可查看菜单/视图/动作/组配置，快速定位 XML/QWeb 来源。
- 报表问题可看容器日志：`docker logs -f educat-odoo`。
- 避免改动 Odoo 核心代码，建议在本仓库维护自定义/修复。

## 常见问题速查
- 报表文件名中文报错：升级 `openeducat_core,openeducat_library`，确保翻译中无全角 `%`/括号。
- 在读证明报 IndexError：已用安全取值 `course_detail_ids[:1]`，升级核心模块即可。
- 翻译未生效：确认系统语言为简体中文，并对相关模块执行升级。
