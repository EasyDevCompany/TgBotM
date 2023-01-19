START_MESSAGE = "Здравствуйте, данный бот помогает вам создавать запросы для" \
                " обработки администратором или сотрудником технической поддержки.\n\n" \
                "Что умеет этот бот:\n" \
                "• создание запросов для обработки сотрудником тех. поддержки/администратором в ЭДО\n" \
                "• отслеживание статуса готовности\n" \
                "• связь с сотрудником, обрабатывающим запрос\n" \
                "• возможность корректировать свой запрос\n" \
                "• возможность отменить некорректный запрос\n\n" \
                "Чтобы начать работу, нажмите кнопку «Начать работу»"

START_SUPPORT = "Данный бот помогает вам обработать запросы от сотрудников компании" \

ADD_SUBOBJECTS = 'Для добавления подобъектов в форме необходимо дать ' \
                 'подробную информацию:\n1) Необходимо выбрать из ' \
                 'предоставленных вариантов главу для подобъекта\n' \
                 '2) Необходимо указать раздел подобъекта\n' \
                 '3) Необходимо указать название подобъекта, который ' \
                 'Вам необходимо добавить в ЭДО\n' \
                 '4)Необходимо указать сортировку\n' \
                 '5) Необходимо выбрать, в каких подсистемах данный\n' \
                 'подобъект должен отображаться после внесения его в ЭДО\n\n' \

SET_CHAPTER = 'Укажите главу: '

ADD_MATERIALS = "Для добавления материалов на остаток в форме необходимо:\n\n" \
                '1) Прикрепить служебную записку, написанную на имя своего руководителя по шаблону,\n' \
                'подписанную Вами и руководителем.\n\n' \
                '2) Выбрать склад, куда необходимо добавить остатки\n' \
                '3) Прикрепить заполненную таблицу Excel по шаблону.\n\n' \
                'В данной Excel таблице необходимо заполнить следующие поля строго согласно наименованиям ' \
                'в ЭДО: титул, объект, код ресурса, наименование, единица измерения, количество, склад\n\n' \
                '4) Указать куда необходимо добавить свободные остатки\n' \
                '5) Укажите на какой объект необходимо резервировать остатки \n' \
                '\n\nшаблоны'

ADD_EDO = 'Для добавления объекта в форме необходимо дать подробную информацию:\n\n' \
          '1) Необходимо прикрепить служебную записку с подписью начальника ' \
          'отдела, в которой указана причина, по которой необходимо добавить ' \
          'объект\n\n2) Необходимо указать название объекта, которое надо ' \
          'добавить в ЭДО\n\n3) Необходимо указать титул объекта\n\n4) Необходимо ' \
          'указать склад, к которому будет прикреплен объект'\
            '\n\nшаблон'

OPEN_EDO = 'Для добавления объекта в форме необходимо дать подробную ' \
           'информацию:\n\n1) Необходимо прикрепить служебную записку, в ' \
           'которой указано, для чего и по какой причине определенному ' \
           'сотруднику необходимо внести правки в доступы его персональный ' \
           'аккаунт\n\n2) Необходимо указать Ф.И.О. сотрудника, которому ' \
           'надо внести корректировки в доступы или события\n\n3) Необходимо ' \
           'указать, доступ к чему нужен данному сотруднику\n\n4) Необходимо ' \
           'в развернутом виде описать, для какой цели сотруднику нужен доступ'\
            '\n\nшаблон'

NOTE = 'Файл служебной записки: '

UPDATE_COEF = 'Укажите наименование, в котором необходимо внести коэффициент пересчета'

NUMBER_BID = 'Укажите номер заявки'

FOR_WHAT_ACS = 'Опишите, для чего сотруднику нужен доступ к функционалу ' \
               '(развернуто описать, что сотрудник хочет сделать)'

EDIT_MOV = 'Для редактирования некорректного перемещения в форме необходимо\n\n' \
           '1) Прикрепить файл служебной записки\n' \
           '2) Указать номер заявки, если перемещение по заявке\n' \
           '3) Указать номер накладного документа\n' \
           '4) Указать исходящий склад (откуда было отправлено)\n' \
           '5) Указать входящий склад \n' \
           '6) Выбрать статус перемещения \n' \
           '7) Выбрать причину корректировки \n' \
           '8) Указать подробное описание'\
            '\n\nшаблон'

EDIT_SHIP = 'Для внесения корректировок в поставку в форме необходимо:\n\n' \
            '1) Прикрепить служебную записку, написанную на имя своего ' \
            'руководителя по шаблону, подписанную Вами и руководителем.\n' \
            '2) Указать номер заявки\n3) Указать номер накладного документа' \
            '\n4) Указать входящий склад\n5) Указать, что необходимо ' \
            'отредактировать в поставке\n6) Подробно описать ошибку в ' \
            'поставке\n7) Прикрепить дополнительные файлы (по необходимости)' \
            '\n\nшаблон'

CHANGE_STATUS_APPLICATION = "Для редактирования статуса заявки необходимо: \n\n" \
                            "1) Прикрепить подписанную служебную записку, в которой\n" \
                            "указана причина смены статуса заявки.\n" \
                            "2) Указать номер заявки, в которой необходимо поменять статус.\n" \
                            "3) Указать, на каком статусе заявка должна оказаться.\n" \
                            "(название статуса должно совпадать с названием в ЭДО)\n" \
                            '\n\nшаблон'

CONVERSION_FACTOR = "Добавление коэффициента пересчета по наименованию\n\n" \
                    "Для внесения нового коэффициента пересчета по\n" \
                    "наименованию необходимо: \n\n" \
                    "1) Указать наименование, которому необходимо внести\n" \
                    "коэффициент пересчета (оно должно полностью совпадать с\n" \
                    "наименованием в ЭДО)\n" \
                    "2) Указать уже прикрепленную единицу измерения и ту, в" \
                    "которую необходимо преобразовать (пример заполнения: шт. (старая ед." \
                    "изм.) - упаковка (новая ед. изм.))\n" \
                    "3) Указать соотношение старой ед. изм. к новой (пример\n" \
                    "заполнения: 10 шт. - 1 упаковка)\n\n" \
                    "Укажите наименование, в котором необходимо внести\n" \
                    "коэффициент пересчета\n"

UPDATE_STORAGE = "Для корректирования склада в заявке необходимо: \n\n" \
                 "1) Указать номер заявки, в которой необходимо поменять склад ПП\n" \
                 "2) Указать, какой склад необходимо поставить в заявке\n" \
                 "3) Указать контактное лицо, которое прикреплено к заявке " \
                 "прикреплен в заявке\n" \
                 "4) Указать адрес склада, который будет прикреплен в заявке\n"

ADD_NAMING = "Для добавления наименований в форме необходимо дать подробную информацию: \n\n" \
             "1) Необходимо указать раздел наименования, который надо добавить в ЭДО\n" \
             "2) Необходимо указать подраздел наименования, который надо добавить в ЭДО\n" \
             "3) Необходимо указать группу наименования, которое надо добавить в ЭДО\n" \
             "4) Необходимо указать наименование, которое будет отображаться в ЭДО\n" \
             "5) Необходимо указать единицу измерения наименования, в которой данный материал будет отображаться\n" \
             '\n\nшаблон'

SECTION_MATERIAL = 'Укажите раздел для материала'

EDIT_SUBOBJECT = "Для редактирования подобъектов необходимо:\n" \
                 "1) Указать подобъект видов работ, который необходимо отредактировать\n" \
                 "2) Указать что необходимо отредактировать" \

SELECT_SUBOBJECT = "Укажите подобъект"

EDIT_SUBOBJECT_TYPE_WORK = "Укажите подобъект видов работ"

ADD_TYPE_WORK = "Для добавления вида работ необходимо:\n" \
                "1) Указать подобъект, в который необходимо добавить вид работ\n" \
                "2) Указать вид работ\n" \
                "3) Указать сортировку данного вида работ\n" \
                "4) Выбрать подсистемы, в которых должен отображаться данный вид работ"

SURE = 'Вы уверены, что все данные верны?'

DESCRIPTION_MOVE = 'Подробное описание редактирования перемещения: '

DESCRIPTION_ERROR = 'Подробное описание ошибки в поставке:'

ADJ_INVOICE = 'Для корректировки оформленной накладной необходимо:\n' \
              '1) Прикрепить подписанную служебную записку, в которой ' \
              'указана причина корректировки\n\n5) Указать номер ' \
              'накладной, в которой необходимо внести корректировки\n\n' \
              '2) Указать номер заявки, к которой принадлежит накладная\n\n' \
              '3) Выбрать, что необходимо отредактировать в накладной\n\n' \
              '4) Указать уточняющие данные\n\n шаблон'

EDIT_TYPE_WORK = "Для редактирования видов работ необходимо:\n" \
                 "1) Указать подобъект видов работ, который необходимо отредактировать\n" \
                 "2) Указать вид работ, который необходимо отредактировать\n" \
                 "3) Указать сортировку выбранного вида работ\n" \
                 "4) Выбрать подсистемы, в которых должен отображаться данный вид работ" \

REQUEST_TYPE = 'Вид запроса'

WHAT_EDIT = 'Что редактировать'

REASON = 'Причина корректировки'

WHICH_OBJECT = 'На какой объект'

TABLE = 'Таблица'

YOUR_CHOISE = 'Ваш выбор: '

NAME_OBJECT = 'Укажите название объекта, который необходимо добавить: '

LOAD_DOC = 'Пожалуйста, загрузите документ'

TITUL = 'Укажите титул объекта: '

ERROR_NUMBERS = 'Название объекта не может состоять только из цифр'

STORAGE_OBJ = 'Укажите склад объекта:'

DATA_OBJ = 'Укажите название нового склада, Ф.И.О ответственного лица и титул'

STORAGE_ERROR = 'Название склада не может состоять только из цифр'

STORAGE_NAME = 'Пожалуйста, напишите название склада'

FIO = 'Введите ФИО'

ROLE = 'Выберите свою роль'

R_TYPE = 'Выберите тип запроса'

REQUEST_NUMBER = 'Укажите номер заявки: '

R_NUMBER_ERROR = 'Пожалуйста, укажите номер заявки цифрами'

INCOME_STORAGE = 'Укажите входящий склад(на который приняли поставку): '

WHAT_EDIT_REQUEST = 'Что необходимо отредактировать в поставке:'

NUMBER_REQUEST_IF = 'Укажите номер заявки, если перемещение по заявке'

INVOICE_NUMBER = 'Укажите номер накладной'

OUTGOING_STORAGE = 'Укажите исходящий склад\n(откуда было отправлено)'

OUTGOING_STORAGE_INCOME = 'Укажите входящий склад\n(куда было отправлено)'

STATUS_GOING = 'Укажите статус перемещения'

FIO_EMPLOYEE = 'Укажите ФИО сотрудника'

ACCESS = 'Укажите, доступ к чему нужен сотруднику'

EDIT_STORAGE = 'Выберите склад, куда необходимо добавить остатки: '

EXCEL_DOC = 'Excel файл с данными по наименованиям по формату: '

SURPLUS = 'Укажите, необходимо ли добавлять остатки на резерв или на свободные остатки'

LOAD_EXCEL = 'Пожалуйста, загрузите Excel документ'

RESERVE = 'Если остатки на резерве, то на какой объект их необходимо резервировать'

SUB_PART = 'Укажите подраздел для материала'

GROUP_MAT = 'Укажите группу для материала'

NAME_MAT = 'Укажите название наименования материала'

UNIT_OF_MEASUREMENT = 'Укажите единицу измерения материала'

COUPLE = 'Если необходимо добавить несколько наименований материалов, прикрепите таблицу по шаблону'

LOAD_OR_MISS = 'Пожалуйста, загрузите документ или нажмите кнопку "Пропустить"'

EDIT_PART = 'Укажите раздел: '

EDIT_SUBPART = 'Укажите название подобъекта: '

EDIT_SORT = 'Укажите cортировку: '

EDIT_SUBSISTEMS = 'Укажите подсистемы, в которых подобъект будет отображаться'

EDIT_WORK = 'Укажите наименование вида работ'

EDIT_DOC_NUMBER = 'Укажите номер накладного документа'

WHAT_EDIT_IN_DOC = 'Выберите, что необходимо отредактировать в накладной'

EDIT_INFO = 'Укажите уточняющую информацию'

EDIT_STATUS = 'Укажите какой статус необходимо поставить заявке'

EDIT_NEW_OLD = 'Укажите старую единицу измерения и новую (на которую необходимо поменять)'

RATIO_OLD_NEW = 'Укажите соотношение старой единицы измерения к новой'

UNIT_ERROR = 'Пожалуйста, укажите единицу измерения не только буквами'

RATIO_ERROR = 'Пожалуйста, укажите соотношение старой единицы измерения к новойя не только буквами'

WHAT_EDIT_EXACTLY = 'Укажите что именно необходимо отредактировать'

EDIT_VIEW_WORK = 'Укажите вид работ'

EDIT_SUBSISTEMS_VIEW_WORK = 'Укажите подсистемы, в которых вид работ будет отображаться'

EDIT_NEW_STORAGE = 'Укажите новый склад доставки'

EDIT_CONTACT_NAME = 'Укажите контактное лицо (Ф.И.О.)'

EDIT_ADDRESS = 'Укажите адрес актуального склада (на который нужно поменять)'

ERROR_CONTACT = 'Введите пожалуйста фамилию, имя и отчество'

ADDRESS_ERROR = 'Пожалуйста, укажите адрес актуального склада'

EDIT_POINT = 'Выберите номер пункта для корректировки: '

WAITING_ANSWER = 'Ваш запрос отправлен сотруднику, ожидайте ответа'

INPUT_REASON = 'Введите причину: '

CHANGE_SUCCESS = 'Изменение прошло успешно'

NO_EXTRA = 'Нет дополнительных файлов'

NO_NEW_BIDS = 'Нет новых заявок'

NEW_COMMENT = 'Введите комментарий: '

SELECT_ITEM = 'Выберите пункт редактирования'

BID_ACCEPT ='Ваша заявка принята'

BID_PROCESSED = 'Ваша заявка обработана'

ACCEPT_SENDING = 'Подтвердите отправку или добавьте ещё файлы'

TEMPLATE_EDITION_NAMING = "шаблон_добавления_наименований_материалов_в_ЭДО.xlsx"

CHANGE_STATUS = "Смена статуса заявки.docx"

ADD_MATERIALS_DOC = "добавление_материалов_на_свободный_остаток.docx"

ADD_MATERIALS_XLSX = "добавление_материалов_на_свободный_остаток.xlsx"

ADD_OBJECT = "Добавление объекта в ЭДО.docx"

OPEN_ACCESS = "Открытие доступов в ЭДО для сотрудников.docx"

EDIT_NOT_CORRECT = "Редактирование некорректного перемещения.docx"

EDIT_SHIPMENT = "Корректировка поставок.docx"

CORR_INV = "Корректировка оформленной накладной.docx"
