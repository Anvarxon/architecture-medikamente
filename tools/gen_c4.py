import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dfdlib import Page, write, X0, Y0, CW, CH, NW, NH

OUT = sys.argv[1]

cx = lambda c: X0 + c * CW + NW // 2
cy = lambda r: Y0 + r * CH + NH // 2
gx = lambda c: X0 + c * CW + NW + (CW - NW) // 2
gy = lambda r: Y0 + r * CH + NH + (CH - NH) // 2

p = Page("C4 L1. Контекст (TO-BE)",
         "C4, уровень 1 — контекст целевой системы «Медикаменте» (TO-BE)",
         "Единая медицинская платформа заменяет Excel, общий диск и ручные операции. "
         "Все внешние взаимодействия проходят через контролируемые шлюзы, а конфиденциальные данные — через PII Vault и PDP.",
         "Цвета: тёмно-синий — пользователи; синий — система в фокусе; серый — внешние системы и организации.")

PEOPLE = [
    ("pat", "Пациент", "Записывается на приём, смотрит свои\nанализы, заключения и договоры", "person"),
    ("rec", "Сотрудник ресепшена", "Ведёт запись, подтверждает визиты,\nоформляет договоры", "person"),
    ("doc", "Медицинский специалист", "Ведёт ЭМК, назначает исследования,\nсмотрит результаты своих пациентов", "person"),
    ("cas", "Кассир", "Принимает оплату,\nработает с кодами услуг", "person"),
    ("acc", "Бухгалтер", "Учёт выручки, кадры, зарплата,\nналоговая отчётность", "person"),
    ("wh", "Сотрудник склада", "Учёт ТМЦ, закупки,\nсписание расходников", "person"),
    ("dpo", "Офицер ИБ / DPO", "Политики доступа, реестр обработки,\nразбор инцидентов, аудит", "person"),
    ("ana", "Аналитик данных / ML-инженер", "BI-отчётность и модели\nтолько на обезличенных данных", "person"),
    ("adm", "Администратор платформы", "Эксплуатация, мониторинг,\nуправление ключами и доступами", "person"),
]

EXT = [
    ("lab", "Лаборатория анализов", "Партнёрское API: заказ исследований\nи выдача результатов по псевдониму", "sysext"),
    ("psp", "Платёжный провайдер / банк-эквайер", "Приём платежей, токен карты;\nданные карт не хранятся в компании", "sysext"),
    ("kkm", "ККМ и ОФД", "Фискализация чеков,\nпередача данных в ФНС", "sysext"),
    ("b1c", "1С:Бухгалтерия предприятия", "Регламентированный учёт,\nклиент-серверный режим", "sysext"),
    ("t1c", "1С:Торговля и склад", "Учёт ТМЦ,\nклиент-серверный режим", "sysext"),
    ("notif", "Провайдер уведомлений", "Push, SMS, голосовой робот\n(договор поручения на обработку)", "sysext"),
    ("bank", "Банк (зарплатный проект)", "Зарплатный реестр\nпо защищённому каналу с ЭП", "sysext"),
    ("fns", "ФНС / СФР", "Отчётность по ТКС", "sysext"),
    ("ca", "Удостоверяющий центр / КриптоПро", "Электронная подпись документов\nи сертификаты ГОСТ TLS", "sysext"),
    ("miac", "Региональный МИАЦ / ЕГИСЗ", "Обмен медицинскими сведениями\n(перспектива)", "sysext"),
]

PW, PH, PGAP = 250, 110, 275
SYS_X, SYS_Y, SYS_W, SYS_H = 300, 430, 1900, 220
TOP_Y, BOT_Y = 120, 800

for i, (nid, name, desc, kind) in enumerate(PEOPLE):
    p.free(nid, kind, "<b>%s</b>\n[Человек]\n%s" % (name, desc), 40 + i * PGAP, TOP_Y, PW, PH)
p.free("sys", "sysfocus",
       "<b>Медицинская платформа «Медикаменте»</b>\n[Программная система]\n"
       "Единая система записи, ЭМК, платежей, интеграций и аналитики. "
       "Реализует Privacy by Design: минимизация данных, псевдонимизация, шифрование, "
       "управление согласиями, авторизация ABAC, аудит доступа и тегирование данных.",
       SYS_X, SYS_Y, SYS_W, SYS_H)
for i, (nid, name, desc, kind) in enumerate(EXT):
    p.free(nid, kind, "<b>%s</b>\n[Внешняя система]\n%s" % (name, desc), 40 + i * PGAP, BOT_Y, PW, PH)


def vlink(src, dst, label, up=True, lx=0, ly=0):
    sx, sy, sw, sh = p.geo[src]
    dx_, dy_, dw, dh = p.geo[dst]
    if up:
        fr = min(0.95, max(0.05, (sx + sw / 2.0 - dx_) / dw))
        an = (0.5, 1, round(fr, 3), 0)
    else:
        fr = min(0.95, max(0.05, (dx_ + dw / 2.0 - sx) / sw))
        an = (round(fr, 3), 1, 0.5, 0)
    p.edge(src, dst, label, an=an, lx=lx, ly=ly)


vlink("pat", "sys", "Запись на приём, просмотр\nсвоих данных\n[HTTPS, TLS 1.3, OIDC + MFA]")
vlink("rec", "sys", "Управление расписанием\n[HTTPS, OIDC + MFA]")
vlink("doc", "sys", "Ведение ЭМК\n[HTTPS, OIDC + MFA]")
vlink("cas", "sys", "Приём оплаты\n[HTTPS]")
vlink("acc", "sys", "Финансовый и кадровый учёт\n[HTTPS]")
vlink("wh", "sys", "Учёт ТМЦ\n[HTTPS]")
vlink("dpo", "sys", "Политики, аудит,\nреестр обработки ПДн\n[HTTPS]")
vlink("ana", "sys", "BI и ML только\nна обезличенных данных\n[HTTPS, SQL]")
vlink("adm", "sys", "Эксплуатация\nи мониторинг\n[HTTPS, SSH]")

vlink("sys", "lab", "Заказ исследования по псевдониму\nи приём результата\n[REST, mTLS, подпись]", up=False)
vlink("sys", "psp", "Оплата и возврат\n[REST, TLS 1.3]", up=False)
vlink("sys", "kkm", "Фискализация чека\n[защищённый шлюз, mTLS]", up=False)
vlink("sys", "b1c", "Проводки и выручка\nбез медицинских данных\n[Kafka, REST]", up=False)
vlink("sys", "t1c", "Движение ТМЦ\n[Kafka, REST]", up=False)
vlink("sys", "notif", "Напоминания и подтверждения\n[REST, TLS]", up=False)
vlink("sys", "bank", "Зарплатный реестр\n[канал банка, ЭП]", up=False)
vlink("sys", "fns", "Отчётность\n[ТКС, ЭП]", up=False)
vlink("sys", "ca", "Подпись документов\n[CAdES, ГОСТ]", up=False)
vlink("sys", "miac", "Обмен медицинскими\nсведениями [REST]", up=False)

p.free("note1", "note",
       "НОВЫЕ БЛОКИ, ОБЕСПЕЧИВАЮЩИЕ PRIVACY BY DESIGN (детализация — на странице «C4 L2»)\n\n"
       "1. IAM (Keycloak) — единая аутентификация OIDC + MFA, отказ от общих учётных записей.\n"
       "2. PDP на OPA — авторизация ABAC/RBAC: «свой пациент», «свой филиал», «своя роль».\n"
       "3. PII Vault + KMS/HSM — токенизация прямых идентификаторов и хранение ключей.\n"
       "4. Consent Service — согласия, цели обработки, отзыв, сроки хранения.\n"
       "5. Data Catalog + Tagging + Lineage — классификация данных и прослеживаемость.\n"
       "6. Audit Log (WORM) + SIEM/DLP — журнал доступа, детект аномалий, контроль утечек.\n"
       "7. Retention Service — автоудаление и crypto-shredding по сроку и по отзыву согласия.\n"
       "8. Egress Gateway — единая точка выхода данных наружу с контрактами и квотами.\n"
       "9. Аналитический слой — Data Lake с обезличиванием: BI, ML и LLM без доступа к ПДн.",
       40, 1000, 1120, 300)
p.free("note2", "legend",
       "ПРИНЦИПЫ, ЗАЛОЖЕННЫЕ В КОНТЕКСТ\n\n"
       "• Privacy by Design и by Default: минимальный набор данных на каждом интерфейсе,\n"
       "  расширение состава данных возможно только через изменение контракта.\n"
       "• Data Minimization: наружу уходит псевдоним, а не ФИО; в финансовый контур —\n"
       "  код услуги, а не диагноз.\n"
       "• Zero Trust: любое обращение (внутреннее и внешнее) проходит аутентификацию,\n"
       "  авторизацию в PDP и журналирование.\n"
       "• Data Lineage: для каждого элемента данных известно происхождение, получатели\n"
       "  и срок хранения — это делает выполнимыми права субъекта ПДн.\n"
       "• Хранение и обработка ПДн граждан РФ — на территории РФ (ст. 18 ч. 5 152-ФЗ).",
       1200, 1000, 1000, 300)
pages = [p]

p = Page("C4 L2. Контейнеры (MVP)",
         "C4, уровень 2 — контейнеры целевой платформы «Медикаменте» (объём MVP + задел на финальное состояние)",
         "Слои: клиентские приложения → периметр и privacy-контроль → доменные сервисы → слой данных → аналитический слой. "
         "Блоки Privacy by Design выделены фиолетовым, аналитический слой — зелёным.",
         "В объём MVP (2 месяца) входят: портал пациента, портал ресепшена, Appointment Service, Notification Service, IAM, PDP, PII Vault, Consent, Audit.")

p.boundary("bcl", "Клиентские приложения", 0, 0, 5, 0, color="#2E6295")
p.boundary("bsec", "Периметр и privacy-контроль (Privacy by Design)", 0, 1, 5, 1, color="#7B1FA2")
p.boundary("bdom", "Доменные сервисы (bounded contexts)", 0, 2, 5, 2, color="#2E6295")
p.boundary("bdata", "Слой данных (операционные хранилища)", 0, 3, 5, 3, color="#B8860B")
p.boundary("bana", "Аналитический слой (privacy-preserving analytics)", 0, 4, 5, 4, color="#2E7D32")

CL = [("cl1", "Портал пациента\n[SPA, TypeScript]"),
      ("cl2", "Мобильное приложение\n[iOS / Android]"),
      ("cl3", "Портал ресепшена\n[SPA]"),
      ("cl4", "Портал врача (ЭМК)\n[SPA]"),
      ("cl5", "Портал кассы\nи бухгалтерии [SPA]"),
      ("cl6", "Кабинет сотрудника\nи админ-консоль [SPA]")]
SEC = [("iam", "IAM\n[Keycloak]\nOIDC, MFA, SSO,\nсервисные учётные записи"),
       ("gw", "API Gateway + WAF\n[Kong / Envoy]\nTLS 1.3, mTLS, rate limit,\nвалидация OpenAPI"),
       ("pdp", "PDP\n[OPA / Rego]\nABAC и RBAC,\nполитики как код"),
       ("consent", "Consent Service\n[Java, Spring]\nсогласия, цели,\nотзыв, сроки"),
       ("vault", "PII Vault + KMS/HSM\n[Vault, ГОСТ-крипто]\nтокенизация,\nкрипто-шреддинг"),
       ("cat", "Data Catalog + Tagging\n[DataHub / OpenMetadata]\nклассы данных,\nData Lineage")]
DOM = [("appt", "Appointment Service\n[Java]\nзапись, слоты,\nнапоминания"),
       ("emr", "EMR + Document Service\n[Java]\nЭМК, назначения,\nдокументы"),
       ("pay", "Payment + Billing\n[Java]\nсчета, оплата,\nвыручка по кодам"),
       ("lab", "Lab Integration\n[Java]\nзаказы и результаты,\nEgress Gateway"),
       ("wms", "Warehouse + Procurement\n[Java]\nТМЦ, закупки"),
       ("hr", "HR + Payroll\n[Java]\nкадры, расчёт ЗП")]
DATA = [("pg", "PostgreSQL (кластер)\nTDE, RLS,\nшифрование полей"),
        ("s3", "S3 Object Storage\nSSE-KMS,\nверсионирование"),
        ("kafka", "Kafka + CDC (Debezium)\nшина событий,\nмежсервисный обмен"),
        ("audit", "Audit Log (WORM)\n[ClickHouse + hash-chain]\nнеизменяемый журнал"),
        ("ret", "Retention Service\nсроки хранения,\nавтоудаление"),
        ("siem", "SIEM + DLP + мониторинг\n[Elastic, VictoriaMetrics]\nалертинг на аномалии")]
ANA = [("clsf", "Движок классификации данных\n[Spark + ML/NER + правила]\nсм. Task6 (C2)"),
       ("lake", "Data Lake / DWH\n[S3 + ClickHouse]\nRaw → Cleansed →\nCurated → Marts"),
       ("etl", "ETL / обезличивание\n[Airflow + Spark]\nмаскирование,\nk-анонимность"),
       ("bi", "BI\n[Superset / Metabase]\nP&L, ABC-анализ,\nзагрузка врачей"),
       ("ml", "ML / AI платформа\n[Feature Store, MLflow]\nобучение только\nна обезличенных данных"),
       ("llm", "LLM-сервисы\n[RAG на внутреннем контуре]\nподсказки врачу,\nсаммари документов")]

for i, (nid, lbl) in enumerate(CL):
    p.node(nid, "container", lbl, i, 0)
for i, (nid, lbl) in enumerate(SEC):
    p.node(nid, "cnt_sec", lbl, i, 1)
for i, (nid, lbl) in enumerate(DOM):
    p.node(nid, "container", lbl, i, 2)
for i, (nid, lbl) in enumerate(DATA):
    p.node(nid, "db" if nid in ("pg", "s3", "audit") else "container", lbl, i, 3)
for i, (nid, lbl) in enumerate(ANA):
    p.node(nid, "cnt_data", lbl, i, 4)

for i, nid in enumerate(("cl1", "cl2", "cl3", "cl4", "cl5", "cl6")):
    p.edge(nid, "gw", "", an=(0.5, 1, round(0.08 + i * 0.168, 3), 0))
p.free("lbl_cl", "sub", "HTTPS, TLS 1.3, токен OIDC — единая точка входа для всех приложений", 700, gy(0) - 26, 900, 20)

p.ctl_edge("gw", "iam", "проверка токена")
p.ctl_edge("gw", "pdp", "запрос решения о доступе")
p.ctl_edge("pdp", "consent", "проверка согласия и цели")
p.ctl_edge("consent", "vault", "срок хранения → крипто-шреддинг")
p.ctl_edge("vault", "cat", "классы данных и теги")

for i, nid in enumerate(("appt", "emr", "pay", "lab", "wms", "hr")):
    p.edge("gw", nid, "", an=(round(0.08 + i * 0.168, 3), 1, 0.5, 0))
p.free("lbl_dom", "sub", "Вызовы доменных сервисов по контрактам OpenAPI (mTLS), после решения PDP",
       700, gy(1) - 26, 900, 20)

p.edge("appt", "pg", "данные по token_id")
p.edge("emr", "s3", "документы")
p.edge("pay", "kafka", "события платежей")
p.edge("lab", "audit", "журнал обращений")
p.edge("wms", "ret", "сроки хранения")
p.edge("hr", "siem", "события доступа")

p.edge("pg", "clsf", "CDC-потоки")
p.edge("s3", "lake", "файлы и документы")
p.edge("kafka", "etl", "события")
p.edge("audit", "bi", "метрики доступа")
p.edge("ret", "ml", "политики хранения")
p.edge("siem", "llm", "алерты и аномалии")
p.free("lbl_ana", "sub",
       "Данные попадают в аналитический слой только после классификации и обезличивания: прямые идентификаторы заменяются токенами, "
       "квазиидентификаторы обобщаются",
       500, gy(3) - 26, 1500, 20)

p.free("mvp", "note",
       "ОБЪЁМ MVP (2 МЕСЯЦА)\n\n"
       "Клиенты: портал пациента, портал ресепшена.\n"
       "Безопасность: API Gateway, IAM (Keycloak), PDP (OPA),\n"
       "Consent Service, PII Vault, Audit Log.\n"
       "Домены: Appointment Service, Notification Service.\n"
       "Данные: PostgreSQL (RLS + шифрование полей), Kafka, WORM-журнал.\n"
       "Аналитика: минимальный Data Lake и BI на обезличенных витринах.\n\n"
       "ФИНАЛЬНОЕ СОСТОЯНИЕ (1 ГОД)\n\n"
       "Мобильное приложение и голосовой робот, ЭМК и документы,\n"
       "платёжный шлюз, интеграция с лабораторией, CRM, HR и ТМЦ,\n"
       "полноценный аналитический слой с ML и LLM,\n"
       "автоматическая проверка релиза на работу с тегированными данными.",
       40, gy(4) + 40, 1180, 300)
p.free("note_keys", "good",
       "КАК ЗАКРЫВАЮТСЯ НФТ\n\n"
       "Безопасность (конфиденциальность): PII Vault, шифрование at rest\n"
       "и in transit, ABAC, WORM-аудит, DLP, Retention Service.\n\n"
       "Масштабируемость: stateless-сервисы в Kubernetes, HPA,\n"
       "шардирование PostgreSQL по филиалам, Kafka как буфер,\n"
       "ClickHouse для аналитики — запас на рост объёма в 5 раз и выше.\n\n"
       "Сопровождаемость: доменные границы, контракты OpenAPI,\n"
       "политики как код (Rego), IaC, единый CI/CD с проверкой\n"
       "работы с тегированными данными.\n\n"
       "Конфигурируемость: политики доступа, сроки хранения, правила\n"
       "классификации и маскирования задаются конфигурацией\n"
       "и справочниками, без доработки кода.",
       1260, gy(4) + 40, 960, 300)
pages.append(p)

write(OUT, pages)
