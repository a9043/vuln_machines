<!--
selectedView — хранит текущий выбранный фильтр по типу машин (готовые, идеи, все).

searchQuery — двусторонне связан с полем поиска, передаётся в дочерний компонент для фильтрации.

MachinesTable — получает фильтр и поисковый запрос через пропсы и эмитит (дочерний компонент сообщает родителю о каком-то действии или изменении) событие выбора машины.
-->

<template>
  <main class="main-content">
    <!-- Блок управления фильтром по типу - идея или готов и поиском -->
    <div class="controls">
      <!-- Выпадающий список для выбора типа отображаемых машин -->
      <select v-model="selectedView" class="view-select">
        <option value="ready">Готовые</option>
        <option value="idea">Идеи</option>
        <option value="all">Все</option>
      </select>

      <!-- Обертка для строки поиска с иконкой -->
      <div class="search-wrapper">
        <!-- Поле ввода для поиска по машинам, двустороннее связывание с searchQuery -->
        <input type="text" v-model="searchQuery" placeholder="Поиск по машинам..." />
        <!-- Иконка лупы, позиционируется поверх поля ввода -->
        <svg class="search-icon" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
          <path d="M21 21l-4.35-4.35M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16z"/>
        </svg>
      </div>
    </div>

    <!-- Компонент таблицы машин, получает фильтр и поисковый запрос через пропсы -->
    <MachinesTable
      :machines="machines"
      :filter-type="selectedView"
      :search-query="searchQuery"
      @select-machine="onSelectMachine"
      @machine-added="fetchMachines"
      @machine-deleted="onMachineDeleted"
    />

  </main>
</template>

<script>
// Импортируем компонент таблицы машин
import MachinesTable from './MachinesTable.vue';
import axios from 'axios';

export default {
  components: { MachinesTable },
  data() {
    return {
      selectedView: 'all',   // Текущий выбранный фильтр по типу машин (ready, idea, all)
      searchQuery: '',       // Текущий поисковый запрос для фильтрации по машинам
      selectedMachine: null, // Выбранная машина (не используется в этом компоненте, для родителя)
      isAdmin: true,         // Флаг, указывающий, админ ли пользователь (влияет на UI) почему он тут - в душе не представляю
      machines: [],        // данные с API
      loading: false,
      error: null,
    };
  },
  created() {
  this.fetchMachines();
  },
  watch: {
  selectedView() {
    this.fetchMachines();
  }
  },
  methods: {
    fetchMachines() {
    this.loading = true;
    this.error = null;

    // Формируем параметры запроса в зависимости от фильтра
    let params = {};
    if (this.selectedView === 'ready') {
      params.type = 'ready';
    } else if (this.selectedView === 'idea') {
      params.type = 'idea';
    }

    axios.get('http://localhost:8000/api/machines/', { params })
      .then(response => {
        this.machines = response.data;
      })
      .catch(error => {
        this.error = 'Ошибка загрузки данных';
        console.error(error);
      })
      .finally(() => {
        this.loading = false;
      });
    },
    // Метод-обработчик события выбора машины из дочернего компонента MachinesTable
    onSelectMachine(machine) {
      // Пробрасываем событие наверх для родительского компонента
      this.$emit('select-machine', machine);
    },
    onMachineDeleted() {
      // Добавляем небольшую задержку для синхронизации
      setTimeout(() => {
        this.fetchMachines();
      }, 100);
      this.$emit('machine-deleted');
    }
  },
  computed: {
  filteredMachines() {
    if (!this.searchQuery) return this.machines;
    const query = this.searchQuery.toLowerCase();
    return this.machines.filter(machine =>
      machine.name.toLowerCase().includes(query) ||
      (machine.description && machine.description.toLowerCase().includes(query))
    );
  }
}
};
</script>

<style scoped>
/* Основные стили для главного контента */
.main-content {
  color: white; 
  padding: 20px 0px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column; 
  height: 95vh; 
}

/* Блок с контролами (фильтр и поиск) */
.controls {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

/* Стили для селекта выбора вида */
.view-select {
  padding: 6px 10px;
  font-size: 1rem;
  margin-right: 20px;
  border-radius: 5px;
  background-color: #2d2d2d; 
  color: #ffffff;
}

/* Обертка для поля поиска и иконки */
.search-wrapper {
  position: relative; 
  flex-grow: 1;    
}

/* Поле ввода поиска */
.search-wrapper input {
  width: 100%;
  padding: 5px 0px;
  font-size: 1rem;
  border-radius: 5px;
  background-color: #2d2d2d; 
  color: white;              
  border: none;
  outline: none;
}

/* Иконка поиска (лупа) */
.search-icon {
  position: absolute;
  right: 10px;
  top: 50%;   
  transform: translateY(-50%);
  pointer-events: none; 
  color: #888;          
}
</style>
