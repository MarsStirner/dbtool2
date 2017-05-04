# coding: utf-8


from deptree.internals.base import DBToolBaseNode


class Main(DBToolBaseNode):
    name = 'tmis-1361'

    depends = ['tmis-1361.rb_symbol_group',
                'tmis-1361.rb_symbol',
                'tmis-1361.insert_symbol_group',
                'tmis-1361.insert_symbols']


class CreaterbSymbolGroup(DBToolBaseNode):
    name = 'tmis-1361.rb_symbol_group'

    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''CREATE TABLE IF NOT EXISTS `rbSymbolGroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(512) NOT NULL DEFAULT '' COMMENT 'Код группы',
  `name` varchar(512) NOT NULL DEFAULT '' COMMENT 'Название символа',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Название групп символов';
''')

class CreaterbSymbol(DBToolBaseNode):
    name = 'tmis-1361.rb_symbol'
    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''CREATE TABLE IF NOT EXISTS `rbSymbol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(512) NOT NULL DEFAULT '' COMMENT 'Код символа',
  `name` varchar(512) NOT NULL DEFAULT '' COMMENT 'Название символа',
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),

  KEY `rbSymbol_rbSymbolGroup_group_fk` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Список символом для вставки в текстовые поля';
''')

class InsertSymbolGroup(DBToolBaseNode):
    name = 'tmis-1361.insert_symbol_group'
    depends = ['tmis-1361.rb_symbol']
    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(u'''INSERT INTO rbSymbolGroup (code, name) VALUES ('math', 'Математические операторы'), ('greek', 'Греческий алфавит');''')


class InsertSymbol(DBToolBaseNode):
    name = 'tmis-1361.insert_symbols'
    depends = ['tmis-1361.rb_symbol_group']
    @classmethod
    def upgrade(cls):
        with cls.connection as c:
            c.execute(
                u'''INSERT INTO rbSymbol (code, name, group_id) VALUES ('2200', 'Для всех', 1),
 ('2201', 'Дополнение', 1),
 ('2202', 'Частичный дифференциал', 1),
 ('2203', 'Там существует', 1),
 ('2204', 'Там не существует', 1),
 ('2205', 'Пустое множество', 1),
 ('2206', 'Инкремент', 1),
 ('2207', 'Оператор набла', 1),
 ('2208', 'Принадлежит множеству', 1),
 ('2209', 'Не принадлежит множеству', 1),
 ('220A', 'Маленький элемент', 1),
 ('220B', 'Содержит в качестве члена', 1),
 ('220C', 'Не содержит в качестве члена', 1),
 ('220D', 'Маленький содержит в качестве члена', 1),
 ('220E', 'Конец доказательства', 1),
 ('220F', 'N-арное произведение', 1),
 ('2210', 'N-арное копроизведение', 1),
 ('2211', 'N-ичное суммирование', 1),
 ('2212', 'Знак минус', 1),
 ('2213', 'Знак минус-плюс', 1),
 ('2214', 'Плюс с точкой', 1),
 ('2215', 'Знак деления', 1),
 ('2216', 'Разность множеств', 1),
 ('2217', 'Оператор звездочки', 1),
 ('2218', 'Кольцевой оператор', 1),
 ('2219', 'Оператор точка маркер списка', 1),
 ('221A', 'Квадратный корень', 1),
 ('221B', 'Кубический корень', 1),
 ('221C', 'Корень четвёртой степени', 1),
 ('221D', 'Пропорционально', 1),
 ('221E', 'Знак бесконечности', 1),
 ('221F', 'Прямой угол', 1),
 ('2220', 'Угол', 1),
 ('2221', 'Измеренный угол', 1),
 ('2222', 'Сферический угол', 1),
 ('2223', 'Разделять', 1),
 ('2224', 'Не разделять', 1),
 ('2225', 'Параллельно', 1),
 ('2226', 'Не параллельно', 1),
 ('2227', 'Логическая и', 1),
 ('2228', 'Логическая или', 1),
 ('2229', 'Пересечение', 1),
 ('222A', 'Союз', 1),
 ('222B', 'Интеграл', 1),
 ('222C', 'Двойной интеграл', 1),
 ('222D', 'Тройной интеграл', 1),
 ('222E', 'Контурный интеграл', 1),
 ('222F', 'Поверхностный интеграл', 1),
 ('2230', 'Интеграл объема', 1),
 ('2231', 'По часовой стрелке интеграл', 1),
 ('2232', 'По часовой стрелке контур интеграл', 1),
 ('2233', 'Против часовой стрелки контур интеграл', 1),
 ('2234', 'Следовательно', 1),
 ('2235', 'Поскольку', 1),
 ('2236', 'Соотношение', 1),
 ('2237', 'Пропорция', 1),
 ('2238', 'Точка минус', 1),
 ('2239', 'Избыток', 1),
 ('223A', 'Геометрическая пропорция', 1),
 ('223B', 'Гомотетичный', 1),
 ('223C', 'Оператор тильды', 1),
 ('223D', 'Обратная тильда', 1),
 ('223E', 'Перевернутая ленивая s', 1),
 ('223F', 'Синусоидальная волна', 1),
 ('2240', 'Сплетение', 1),
 ('2241', 'Не тильда', 1),
 ('2242', 'Минус тильда', 1),
 ('2243', 'Асимптотически равный', 1),
 ('2244', 'Не асимптотически равный', 1),
 ('2245', 'Конгруэнтность (геометрическое равенство)', 1),
 ('2246', 'Приблизительно, но не фактически равный', 1),
 ('2247', 'Ни приблизительно, ни фактически равный', 1),
 ('2248', 'Почти равный', 1),
 ('2249', 'Не почти равный', 1),
 ('224A', 'Почти равный или равный', 1),
 ('224B', 'Тройная тильда', 1),
 ('224C', 'Все равны', 1),
 ('224D', 'Эквивалентный', 1),
 ('224E', 'Геометрически эквивалентный', 1),
 ('224F', 'Различие между', 1),
 ('2250', 'Приближается к пределу', 1),
 ('2251', 'Геометрически равный', 1),
 ('2252', 'Приблизительно равный или образ', 1),
 ('2253', 'Образ или приблизительно равный', 1),
 ('2254', 'Двоеточие равно', 1),
 ('2255', 'Равно двоеточие', 1),
 ('2256', 'Кольцо в равно', 1),
 ('2257', 'Кольцо равно', 1),
 ('2258', 'Соответствует', 1),
 ('2259', 'Оценка', 1),
 ('225A', 'равноугольный', 1),
 ('225B', 'Звезда равно', 1),
 ('225C', 'Равно по определению', 1),
 ('225D', 'Равно по определению', 1),
 ('225E', 'Измеренный', 1),
 ('225F', 'Может быть равно', 1),
 ('2260', 'Не равный', 1),
 ('2261', 'Идентичный, тождество', 1),
 ('2262', 'Не идентичный', 1),
 ('2263', 'Строго эквивалентный', 1),
 ('2264', 'Меньше или равный', 1),
 ('2265', 'Больше чем или равно', 1),
 ('2266', 'Меньше чем над равно', 1),
 ('2267', 'Больше, чем над равно', 1),
 ('2268', 'Менее чем, но не равны', 1),
 ('2269', 'Больше чем, но не равны', 1),
 ('226A', 'Гораздо меньше, чем', 1),
 ('226B', 'Гораздо больше, чем', 1),
 ('226C', 'Между', 1),
 ('226D', 'Не эквивалентный', 1),
 ('226E', 'Не меньше чем', 1),
 ('226F', 'Не больше чем', 1),
 ('2270', 'Ни меньше, ни равный', 1),
 ('2271', 'Ни больше, ни равный', 1),
 ('2272', 'Меньше чем или эквивалентный', 1),
 ('2273', 'Больше чем или эквивалентный', 1),
 ('2274', 'Ни меньше чем ни эквивалентный', 1),
 ('2275', 'Ни больше чем ни эквивалентный', 1),
 ('2276', 'Меньше чем или больше чем', 1),
 ('2277', 'Больше чем или меньше чем', 1),
 ('2278', 'Ни меньше чем ни больше чем', 1),
 ('2279', 'Ни больше чем ни меньше чем', 1),
 ('227A', 'Предшествовать', 1),
 ('227B', 'Преуспевать', 1),
 ('227C', 'Предшествует или равный', 1),
 ('227D', 'Преуспевает или равный', 1),
 ('227E', 'Предшествует или эквивалентный', 1),
 ('227F', 'Преуспевает или эквивалентный', 1),
 ('2280', 'Не предшествует', 1),
 ('2281', 'Не преуспевает', 1),
 ('2282', 'Подмножество', 1),
 ('2283', 'Супермножество', 1),
 ('2284', 'Не подмножество', 1),
 ('2285', 'Не супермножество', 1),
 ('2286', 'Подмножество или равный', 1),
 ('2287', 'Супермножество или равный', 1),
 ('2288', 'Ни подмножество, ни равный', 1),
 ('2289', 'Ни супермножество ни равный', 1),
 ('228A', 'Подмножества с не равным', 1),
 ('228B', 'Супермножество с не равным', 1),
 ('228C', 'Мультимножество', 1),
 ('228D', 'Умножение мультимножества', 1),
 ('228E', 'Союз мультимножества', 1),
 ('228F', 'Квадратное изображение', 1),
 ('2290', 'Квадратный оригинал', 1),
 ('2291', 'Квадратное изображение или равный', 1),
 ('2292', 'Квадратный оригинал или равный', 1),
 ('2293', 'Квадратная крышка', 1),
 ('2294', 'Квадратная чашка', 1),
 ('2295', 'Плюс в круге', 1),
 ('2296', 'Минус в круге', 1),
 ('2297', 'Время в круге', 1),
 ('2298', 'Черта деления в круге', 1),
 ('2299', 'Оператор точка в круге', 1),
 ('229A', 'Оператор круг в круге', 1),
 ('229B', 'Оператор звездочки в круге', 1),
 ('229C', 'Равно в круге', 1),
 ('229D', 'Тире в круге', 1),
 ('229E', 'Плюс в квадрате', 1),
 ('229F', 'Минус в квадрате', 1),
 ('22A0', 'Время в квадрате', 1),
 ('22A1', 'Оператор точка в квадрате', 1),
 ('22A2', 'Кнопка вправо', 1),
 ('22A3', 'Кнопка влево', 1),
 ('22A4', 'Кнопка вниз', 1),
 ('22A5', 'Кнопка вверх', 1),
 ('22A6', 'Утверждение', 1),
 ('22A7', 'Модель', 1),
 ('22A8', 'Истина', 1),
 ('22A9', 'Сила', 1),
 ('22AA', 'Тройная вертикальная черта крестовина справа', 1),
 ('22AB', 'Двойная вертикальная черта двойная крестовина справа', 1),
 ('22AC', 'Не доказывает', 1),
 ('22AD', 'Не верный', 1),
 ('22AE', 'Не вызывает', 1),
 ('22AF', 'Дважды инвертированная вертикальная черта удваивают правую крестовину', 1),
 ('22B0', 'Предшествует под отношением', 1),
 ('22B1', 'Преуспевает под отношением', 1),
 ('22B2', 'Нормальная подгруппа', 1),
 ('22B3', 'Содержит как нормальная подгруппа', 1),
 ('22B4', 'Нормальная подгруппа или равный', 1),
 ('22B5', 'Содержит как нормальная подгруппа или равный', 1),
 ('22B6', 'Оригинальный из', 1),
 ('22B7', 'Изображение', 1),
 ('22B8', 'Мультикарта', 1),
 ('22B9', 'Эрмитово сопряженная матрица', 1),
 ('22BA', 'Вставлять', 1),
 ('22BB', 'Исключающее ИЛИ', 1),
 ('22BC', 'Не-и', 1),
 ('22BD', 'также не', 1),
 ('22BE', 'Правый угол с дугой', 1),
 ('22BF', 'Прямоугольный треугольник', 1),
 ('22C0', 'N-ичная логическая и', 1),
 ('22C1', 'N-ичная логическая или', 1),
 ('22C2', 'N-ичное пересечение', 1),
 ('22C3', 'N-ичное объединение', 1),
 ('22C4', 'Алмазный оператор', 1),
 ('22C5', 'Точечный оператор', 1),
 ('22C6', 'Оператор звёздочка', 1),
 ('22C7', 'Времена подразделения', 1),
 ('22C8', 'Галстук-бабочка', 1),
 ('22C9', 'Полупрямое произведение с левым нормальным множителем', 1),
 ('22CA', 'Полупрямое произведение с правым нормальным множителем', 1),
 ('22CB', 'Левое полупрямое произведение', 1),
 ('22CC', 'Правое полупрямое произведение', 1),
 ('22CD', 'Обратная тильда равно', 1),
 ('22CE', 'Вьющийся логический или', 1),
 ('22CF', 'Вьющийся логический и', 1),
 ('22D0', 'Двойное подмножество', 1),
 ('22D1', 'Двойное супермножество', 1),
 ('22D2', 'Двойное пересечение', 1),
 ('22D3', 'Двойное объединение', 1),
 ('22D4', 'Вилы', 1),
 ('22D5', 'Равно и параллельно', 1),
 ('22D6', 'Менее чем с точкой', 1),
 ('22D7', 'Больше чем с точкой', 1),
 ('22D8', 'Много меньше чем', 1),
 ('22D9', 'Много больше чем', 1),
 ('22DA', 'Меньше и равно или большей чем', 1),
 ('22DB', 'Больше и равно или меньше чем', 1),
 ('22DC', 'Равно или меньше чем', 1),
 ('22DD', 'Равно или больше чем', 1),
 ('22DE', 'Равно или предшествует', 1),
 ('22DF', 'Равно или успешно', 1),
 ('22E0', 'Не предшествует или равно', 1),
 ('22E1', 'Не успешно или равно', 1),
 ('22E2', 'Не квадратный образ или равно', 1),
 ('22E3', 'Не квадратный оригинал или равно', 1),
 ('22E4', 'Квадратное изображение или не равно', 1),
 ('22E5', 'Квадратный оригинал или не равно', 1),
 ('22E6', 'Меньше чем, но не эквивалентны', 1),
 ('22E7', 'Больше чем, но не эквивалентны', 1),
 ('22E8', 'Предшествует, но не эквивалентны', 1),
 ('22E9', 'Успешно, но не эквивалентны', 1),
 ('22EA', 'Не нормальная подгруппа', 1),
 ('22EB', 'Не содержит в качестве нормальной подгруппы', 1),
 ('22EC', 'Не нормальная подгруппа или равно', 1),
 ('22ED', 'Не содержит в качестве нормальной подгруппы или равно', 1),
 ('22EE', 'Вертикальное многоточие (троеточие)', 1),
 ('22EF', 'Многоточие на средней линии', 1),
 ('22F0', 'Диагональное многоточие вверх направо', 1),
 ('22F1', 'Диагональное многоточие вниз направо', 1),
 ('22F2', 'Элемент с длинной горизонтальной чертой', 1),
 ('22F3', 'Элемент с вертикальной чертой и горизонтальной черточкой в конце', 1),
 ('22F4', 'Малый элемент с вертикальной чертой и горизонтальной черточкой в конце', 1),
 ('22F5', 'Элемент с точкой сверху', 1),
 ('22F6', 'Элемент с чертой', 1),
 ('22F7', 'Малый элемент с чертой', 1),
 ('22F8', 'Элемент подчеркнутый', 1),
 ('22F9', 'Элемент с двумя горизонтальными чертами', 1),
 ('22FA', 'Содержит в себе длинные горизонтальные черточки', 1),
 ('22FB', 'Содержит в себе горизонтальную черту с вертикальной черточкой на конце', 1),
 ('22FC', 'Малый элемент содержит в себе горизонтальную черту с вертикальной черточкой на конце', 1),
 ('22FD', 'Черта сверху', 1),
 ('22FE', 'Малый элемент с чертой сверху', 1),
 ('22FF', 'Z обозначение принадлежность', 1),
 ('0370', 'Греческая заглавная буква хета', 2),
 ('0371', 'Греческая строчная буква хета', 2),
 ('0372', 'Греческая заглавная архаичная буква сампи', 2),
 ('0373', 'Греческая строчная архаичная буква сампи', 2),
 ('0374', 'Греческий знак цифры', 2),
 ('0375', 'Греческая нижний знак цифры', 2),
 ('0376', 'Греческая заглавная буква памфилийская дигамма', 2),
 ('0377', 'Греческая строчная буква памфилийская дигамма', 2),
 ('037A', 'Греческая йота индекс', 2),
 ('037B', 'Греческий маленький обратный полулунный символ сигма', 2),
 ('037C', 'Греческий маленький пунктирный полулунный символ сигма', 2),
 ('037D', 'Греческий маленький обратный пунктирный полулунный сигма символ', 2),
 ('037E', 'Греческий знак вопроса', 2),
 ('037F', 'Греческая заглавная Йота', 2),
 ('0384', 'Греческая тоносос', 2),
 ('0385', 'Греческая диалитика тонос', 2),
 ('0386', 'Греческая заглавная буква альфа с тонос', 2),
 ('0387', 'Греческая центрировання точка', 2),
 ('0388', 'Греческая заглавная буква эпсилон с тонос', 2),
 ('0389', 'Греческая заглавная буква эта с тонос', 2),
 ('038A', 'Греческая заглавная буква йота с тонос', 2),
 ('038C', 'Греческая заглавная буква омикрон с тонос', 2),
 ('038E', 'Греческая заглавная буква ипсилон с тонос', 2),
 ('038F', 'Греческая заглавная буква омега с тонос', 2),
 ('0390', 'Греческая строчная буква йота с диалитика и тонос', 2),
 ('0391', 'Греческая заглавная буква альфа', 2),
 ('0392', 'Греческая заглавная буква бета', 2),
 ('0393', 'Греческая заглавная буква гамма', 2),
 ('0394', 'Греческая заглавная буква дельта', 2),
 ('0395', 'Греческая заглавная буква эпсилон', 2),
 ('0396', 'Греческая заглавная буква дзета', 2),
 ('0397', 'Греческая заглавная буква эта', 2),
 ('0398', 'Греческая заглавная буква тета', 2),
 ('0399', 'Греческая заглавная буква йота', 2),
 ('039A', 'Греческая заглавная буква каппа', 2),
 ('039B', 'Греческая заглавная буква лямбда', 2),
 ('039C', 'Греческая заглавная буква мю', 2),
 ('039D', 'Греческая заглавная буква ню', 2),
 ('039E', 'Греческая заглавная буква кси', 2),
 ('039F', 'Греческая заглавная буква омикрон', 2),
 ('03A0', 'Греческая заглавная буква пи', 2),
 ('03A1', 'Греческая заглавная буква ро', 2),
 ('03A3', 'Греческая заглавная буква сигма', 2),
 ('03A4', 'Греческая заглавная буква тау', 2),
 ('03A5', 'Греческая заглавная буква ипсилон', 2),
 ('03A6', 'Греческая заглавная буква фи', 2),
 ('03A7', 'Греческая заглавная буква хи', 2),
 ('03A8', 'Греческая заглавная буква пси', 2),
 ('03A9', 'Греческая заглавная буква омега', 2),
 ('03AA', 'Греческая заглавная буква йота с диалитика', 2),
 ('03AB', 'Греческая заглавная буква ипсилон с диалитика', 2),
 ('03AC', 'Греческая строчная буква альфа с тонос', 2),
 ('03AD', 'Греческая строчная буква эпсилон с тонос', 2),
 ('03AE', 'Греческая строчная буква эта с тонос', 2),
 ('03AF', 'Греческая строчная буква йота с тонос', 2),
 ('03B0', 'Греческая строчная буква ипсилон с диалитика и тонос', 2),
 ('03B1', 'Греческая строчная буква альфа', 2),
 ('03B2', 'Греческая строчная буква бета', 2),
 ('03B3', 'Греческая строчная буква гамма', 2),
 ('03B4', 'Греческая строчная буква дельта', 2),
 ('03B5', 'Греческая строчная буква эпсилон', 2),
 ('03B6', 'Греческая строчная буква дзета', 2),
 ('03B7', 'Греческая строчная буква эта', 2),
 ('03B8', 'Греческая строчная буква тета', 2),
 ('03B9', 'Греческая строчная буква йота', 2),
 ('03BA', 'Греческая строчная буква каппа', 2),
 ('03BB', 'Греческая строчная буква лямбда', 2),
 ('03BC', 'Греческая строчная буква мю', 2),
 ('03BD', 'Греческая строчная буква ню', 2),
 ('03BE', 'Греческая строчная буква кси', 2),
 ('03BF', 'Греческая строчная буква омикрон', 2),
 ('03C0', 'Греческая строчная буква пи', 2),
 ('03C1', 'Греческая строчная буква ро', 2),
 ('03C2', 'Греческая строчная буква окончательная сигма', 2),
 ('03C3', 'Греческая строчная буква сигма', 2),
 ('03C4', 'Греческая строчная буква тау', 2),
 ('03C5', 'Греческая строчная буква ипсилон', 2),
 ('03C6', 'Греческая строчная буква фи', 2),
 ('03C7', 'Греческая строчная буква хи', 2),
 ('03C8', 'Греческая строчная буква пси', 2),
 ('03C9', 'Греческая строчная буква омега', 2),
 ('03CA', 'Греческая строчная буква йота с диалитика', 2),
 ('03CB', 'Греческая строчная буква ипсилон с диалитика', 2),
 ('03CC', 'Греческая строчная буква омикрон с тонос', 2),
 ('03CD', 'Греческая строчная буква ипсилон с тонос', 2),
 ('03CE', 'Греческая строчная буква омега с тонос', 2),
 ('03CF', 'Греческий заглавный символ кай', 2),
 ('03D0', 'Греческий символ бета', 2),
 ('03D1', 'Греческий символ тета', 2),
 ('03D2', 'Греческий символ ипсилон с крючком', 2),
 ('03D3', 'Греческий символ ипсилон с акутом и крючком', 2),
 ('03D4', 'Греческий символ ипсилон с диэрезисом и крючком', 2),
 ('03D5', 'Греческий символ фи', 2),
 ('03D6', 'Греческий символ пи', 2),
 ('03D7', 'Греческий символ кай', 2),
 ('03D8', 'Греческая архаичная буква коппа', 2),
 ('03D9', 'Греческая строчная архаичная буква коппа', 2),
 ('03DA', 'Греческая буква стигма', 2),
 ('03DB', 'Греческая строчная буква стигма', 2),
 ('03DC', 'Греческая буква дигамма', 2),
 ('03DD', 'Греческая строчная буква дигамма', 2),
 ('03DE', 'Греческая буква коппа', 2),
 ('03DF', 'Греческая строчная буква коппа', 2),
 ('03E0', 'Греческая буква сампи', 2),
 ('03E1', 'Греческая строчная буква сампи', 2),
 ('03E2', 'Коптская заглавная буква шай', 2),
 ('03E3', 'Коптская строчная буква шай', 2),
 ('03E4', 'Коптская заглавная буква фай', 2),
 ('03E5', 'Коптская строчная буква фай', 2),
 ('03E6', 'Коптская заглавная буква хай', 2),
 ('03E7', 'Коптская строчная буква хай', 2),
 ('03E8', 'Коптская заглавная буква хори', 2),
 ('03E9', 'Коптская строчная буква хори', 2),
 ('03EA', 'Коптская заглавная буква джанджа', 2),
 ('03EB', 'Коптская строчная буква джанджа', 2),
 ('03EC', 'Коптская заглавная буква чима', 2),
 ('03ED', 'Коптская строчная буква кима', 2),
 ('03EE', 'Коптская заглавная буква ти', 2),
 ('03EF', 'Коптская строчная буква ти', 2),
 ('03F0', 'Греческий символ каппа', 2),
 ('03F1', 'Греческий символ ро', 2),
 ('03F2', 'Греческий символ сигма в виде полумесяца', 2),
 ('03F3', 'Греческая буква йот', 2),
 ('03F4', 'Греческий заглавный тета символ', 2),
 ('03F5', 'Греческий символ эпсилон', 2),
 ('03F6', 'Греческий  обратный символ эпсилон в виде полумесяца', 2),
 ('03F7', 'Греческая заглавная буква шо', 2),
 ('03F8', 'Греческая строчная буква шо', 2),
 ('03F9', 'Греческий заглавный символ сигма в виде полумесяца', 2),
 ('03FA', 'Греческая заглавная буква сан', 2),
 ('03FB', 'Греческая строчная буква сан', 2),
 ('03FC', 'Греческий символ ро со штрихом', 2),
 ('03FD', 'Греческий заглавный обратный символ сигма в виде полумесяца', 2),
 ('03FE', 'Греческий заглавный символ сигма в виде полумесяца с точкой', 2),
 ('03FF', 'Греческий заглавный перевёрнутый символ сигма в виде полумесяца с точкой', 2);
''')
