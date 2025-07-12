<!--
filters — массив с описанием всех фильтров, где каждый фильтр может иметь опции (варианты выбора) или быть простым чекбоксом.

openFilterId — хранит id фильтра, у которого открыто выпадающее меню опций.

toggleFilterOptions(id) — переключает открытие/закрытие меню опций для фильтра.

onOptionChange(filter) — обновляет состояние активности фильтра в зависимости от выбранных опций.

В шаблоне для фильтров без опций отображается простой чекбокс, для фильтров с опциями — заголовок с выпадающим меню.
-->

<template>
  <aside class="filters-panel">
    <h2 class="title">Фильтры</h2>
    <ul class="filters-list">
      <!-- Перебираем все фильтры из массива filters -->
       <!-- Добавляем класс active, если фильтр активен -->
    <li v-for="filter in filters" :key="filter.id" :class="{'active': filter.active}">

      <!-- Зеленая полоска слева, показывается если фильтр активен -->
        <div class="active-bar" v-if="filter.active"></div>

        <!-- Заголовок фильтра, кликабельный для открытия/закрытия опций -->
        <div class="filter-header" @click="toggleFilterOptions(filter.id)">

          <!-- Если у фильтра нет опций, показываем чекбокс и название -->
        <label v-if="!filter.options.length">
            <input type="checkbox" v-model="filter.active" />
            {{ filter.name }}
        </label><!-- Если есть опции, показываем название и стрелочку --> 
        <span v-else>
            {{ filter.name }}
            <svg class="arrow-icon" :class="{open: openFilterId === filter.id}" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
        </span>
        </div>

        <!-- Выпадающее меню с вариантами фильтра, показывается если открыт этот фильтр и есть опции -->
        <div v-if="openFilterId === filter.id && filter.options.length" class="options-dropdown">
        <label v-for="option in filter.options" :key="option" class="option-item">
            <input
            type="checkbox"
            :value="option"
            v-model="filter.selectedOptions"
            @change="onOptionChange(filter)"
            />
            {{ option }}
        </label>
        </div>
    </li>
    </ul>

  </aside>
</template>

<script>
export default {
  name: 'FiltersPanel',
  data() {
  return {
    // Массив фильтров с их параметрами
    filters: [
      { id: 1, name: 'Название', active: false, options: [], selectedOptions: [] },
      { id: 2, name: 'ID', active: false, options: [], selectedOptions: [] },
      { id: 3, name: 'Тип', active: false, options: ['ready', 'idea'], selectedOptions: [] },
      { id: 4, name: 'Статус', active: false, options: ['Используется', 'Не используется'], selectedOptions: [] },
      { id: 5, name: 'Теги', active: false, options: [], selectedOptions: [] },
      { id: 6, name: 'Описание', active: false, options: [], selectedOptions: [] },
      { id: 7, name: "WriteUp'ы", active: false, options: [], selectedOptions: [] },
      { id: 8, name: 'ОС', active: false, options: ['Windows', 'Linux', 'Android', 'Mac'], selectedOptions: [] },
      { id: 9, name: 'Графика в ОС', active: false, options: ['Да', 'Нет'], selectedOptions: [] },
      { id: 10, name: 'Кейсы', active: false, options: [], selectedOptions: [] },
      { id: 11, name: 'Список кейсов', active: false, options: [], selectedOptions: [] },
      { id: 12, name: 'СЗИ', active: false, options: [], selectedOptions: [] },
      {
        id: 13,
        name: 'Версии ПО',
        active: false,
        options: [
          'ESXI: 6.7',
          'ОС: Ubuntu 20.04',
          'MySQL: 5.7',
        ],
        selectedOptions: [],
      },
      { id: 14, name: 'Создатель', active: false, options: [], selectedOptions: [] },
    ],

    // id фильтра, у которого в данный момент открыто выпадающее меню с опциями
    openFilterId: null,
  };
},

  methods: {
        // Метод переключения открытия/закрытия выпадающего меню фильтра
  toggleFilterOptions(id) {
    if (this.openFilterId === id) {
      this.openFilterId = null;
    } else {
      this.openFilterId = id;
    }
  },

  // Метод вызывается при изменении выбора опций в фильтре
  onOptionChange(filter) {
    // Если выбраны опции — считаем фильтр активным
    filter.active = filter.selectedOptions.length > 0;
    // Здесь можно добавить логику эмита события с выбранными фильтрами
    this.$emit('filters-changed', this.filters);
  },
},

};
</script>


<style scoped>
/* Основные стили панели фильтров */
.filters-panel {
  background-color: #141414;
  border-radius: 15px;
  color: white;
  box-sizing: border-box;
  position: sticky;
  top: 0; /* Фиксируем панель сверху при прокрутке */
  height: 90vh; /* Ограничиваем высоту панели для прокрутки */
  overflow-y: auto; /* Включаем вертикальную прокрутку, если содержимое не помещается */
  padding: 2%;
  margin: 1%;
}

/* Заголовок панели */
.title {
  font-size: 1.2rem;
  font-weight: 700;
}

/* Список фильтров */
.filters-list {
  list-style: none;
  padding: 0;
  margin: 0;
  color: #c9c9c9;
}

/* Элемент списка фильтра */
.filters-list li {
  position: relative;
  margin-bottom: 8px;
  cursor: pointer;
  user-select: none;
  border-radius: 4px;
  transition: background-color 0.1s ease;
  padding-left: 10px;
}

/* Подсветка активного фильтра */
.filters-list li.active {
  background-color: #313131;
}

/* Метка занимает всю ширину элемента и реагирует на клик */
.filters-list label {
  padding: 5px 0px;
  display: block;
  width: 100%;
  cursor: pointer;
  user-select: none;
  padding-left: 0;
}

/* Скрываем стандартный чекбокс, но он остаётся доступным для взаимодействия */
input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  margin: 0;
  padding: 0;
}

/* Зеленая полоска слева для активного фильтра */
.active-bar {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: #8aff00; /* кислотно-зеленый цвет */
  border-radius: 2px 0 0 2px;
}

/* Отступ справа для чекбокса (хотя он скрыт) */
input[type="checkbox"] {
  margin-right: 8px;
}

/* Заголовок фильтра — флекс контейнер для выравнивания текста и стрелочки */
.filter-header {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  position: relative;
}

/* Стрелочка для раскрытия опций */
.arrow-icon {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

/* Поворот стрелочки при открытом состоянии */
.arrow-icon.open {
  transform: rotate(180deg);
}

/* Выпадающее меню с вариантами выбора */
.options-dropdown {
  background-color: #222;
  margin: 5px 15px 10px 15px;
  border-radius: 6px;
  padding: 8px 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  max-height: 150px; /* Ограничение по высоте с прокруткой */
  overflow-y: auto;
}

/* Отдельный вариант в выпадающем меню */
.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 6px;
  color: #c9c9c9;
  cursor: pointer;
}

/* Отступ справа для чекбокса внутри опции */
.option-item input[type="checkbox"] {
  margin-right: 8px;
}
</style>