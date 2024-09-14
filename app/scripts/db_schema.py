# from sqlalchemy_schemadisplay import create_schema_graph
# from sqlalchemy import MetaData
# from app.core.database import engine  # Импортируем ваш движок SQLAlchemy
#
# # Создаем объект MetaData, используя ваш движок
# metadata = MetaData(bind=engine)
#
# # Генерируем диаграмму
# graph = create_schema_graph(metadata=metadata,
#                             show_datatypes=True,  # Показывать типы данных колонок
#                             show_indexes=True,    # Показывать индексы
#                             rankdir='LR',         # Опция отображения графа (TB - сверху вниз, LR - слева направо)
#                             concentrate=False)     # Упрощение ребер
#
# # Сохраняем граф в файл
# graph.write_png('schema.png')