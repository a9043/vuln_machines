<!--
Таблица с машинами: отображает список с возможностью фильтрации и выбора машины.

Кнопка «Добавить»: открывает модальное окно для добавления новой машины.

Модальное окно: форма с полями для всех параметров машины, включая динамический список кейсов и версий ПО.

Двустороннее связывание (v-model): связывает поля формы с объектом form в data.

Методы управления модальным окном и формой: открытие, закрытие, сброс формы, добавление/удаление кейсов и кастомных версий ПО.
-->

<template>
  <div class="table-container">
    <!-- Заголовок таблицы с названием и кнопкой добавления новой машины -->
    <div class="table-header">
      <div class="left-title">Компьютеры</div>
      <button class="add-button" @click="openAddModal">
        <!-- Иконка плюса на кнопке -->
        <svg class="plus-icon" viewBox="0 0 24 24" width="20" height="20" fill="999999">
          <path d="M19 13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
        </svg>
      </button>
    </div>
    
    <!-- Таблица с машинами -->
    <table class="machines-table">
      <thead>
        <tr>
          <th></th> 
          <th>Название</th>
          <th>ID</th>
          <th>Статус</th>
          <th>ОС</th>
          <th>Тип</th> 
        </tr>
      </thead>
      <tbody>
        <!-- Перебор отфильтрованных машин -->
        <tr
          v-for="machine in filteredMachines"
          :key="machine.id"
          @click="selectMachine(machine)" 
          :class="{ selected: selectedMachineId === machine.id }" 
        >
          <td><OSIcon :os="machine.os" /></td> <!-- Иконка ОС -->
          <td>{{ machine.name }}</td>
          <td>{{ machine.vuln_id }}</td>
          <td>{{ machine.status }}</td>
          <td>{{ machine.os }}</td>
          <td>{{ machine.type === 'ready' ? 'Готовая' : 'Идея' }}</td> <!-- Отображение типа -->
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно добавления новой машины -->
    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Добавить новую машину</h3>
        <form @submit.prevent="submitForm">
          <!-- Поля формы с двусторонним связыванием с объектом form -->
          <label for="name">Название</label>
          <input id="name" v-model="form.name" type="text" placeholder="Введите название" required/>

          <label for="vuln_id">ID уязвимости</label>
          <input id="vuln_id" v-model="form.vuln_id" type="text" placeholder="Формат Vuln-XXX (например: Vuln-001)" required/>

          <label for="type">Тип</label>
          <select id="type" v-model="form.type">
            <option value="ready">Готовая</option>
            <option value="idea">Идея</option>
          </select>

          <label for="status">Статус</label>
          <select id="status" v-model="form.status">
            <option value="Используется">Используется</option>
            <option value="Не используется">Не используется</option>
          </select>

          <label for="wiki_link">Ссылка на Wiki</label>
          <input id="wiki_link" v-model="form.wiki_link" type="url" placeholder="https://example.com" />

          <label for="tags">Теги (через запятую)</label>
          <input id="tags" v-model="form.tagsString" type="text" placeholder="RCE, SQLi" />

          <label for="description">Описание</label>
          <textarea id="description" v-model="form.description" required></textarea>

          <label for="writeups">WriteUp'ы (через запятую)</label>
          <input id="writeups" v-model="form.writeupsString" type="text" placeholder="WriteUp 1, WriteUp 2" />

          <label for="os">ОС</label>
          <select id="os" v-model="form.os" required>
            <option value="Windows">Windows</option>
            <option value="Linux">Linux</option>
            <option value="Android">Android</option>
            <option value="MacOS">MacOS</option>
          </select>

          <label for="has_gui">Графика в ОС</label>
          <select id="has_gui" v-model="form.has_gui">
            <option :value="true">Да</option>
            <option :value="false">Нет</option>
          </select>

          <label for="cases_count">Количество кейсов</label>
          <input id="cases_count" v-model.number="form.cases_count" type="number" min="0" />

          <label>Список кейсов</label>
          <input id="cases_list" v-model="form.casesListString" type="text" placeholder="Кейс1, Кейс2" />

          <label for="detected_in">В каких СЗИ детектируется (через запятую)</label>
          <input id="detected_in" v-model="form.detectedInString" type="text" placeholder="SIEM, EDR" />

          <label for="security_tools">Средства защиты (через запятую)</label>
          <input id="security_tools" v-model="form.security_toolsString" type="text" placeholder="SIEM, EDR, IDS" />

          <label for="esxi_version">Версия ESXi</label>
          <input id="esxi_version" v-model="form.esxi_version" type="text" />

          <label for="os_version">Версия ОС</label>
          <input id="os_version" v-model="form.os_version" type="text" />

          <label for="additional_versions">Дополнительные версии ПО</label>
          <textarea id="additional_versions" v-model="form.additional_versions"></textarea>

          <!-- Кнопки управления модальным окном -->
          <div class="modal-buttons">
            <button type="button" @click="closeAddModal">Отмена</button>
            <button type="submit">Добавить</button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
import OSIcon from './OSIcon.vue';

export default {
  name: 'MachinesTable',
  components: { OSIcon },
  props: {
    machines: Array,
    filterType: String,
    searchQuery: String,
  },
  data() {
  return {
    showAddModal: false,
    selectedMachineId: null,
    form: {
        name: '',
        vuln_id: '',
        type: 'ready',
        status: 'Используется',
        wiki_link: '',
        tagsString: '',
        description: '',
        writeupsString: '',
        os: 'Windows',
        has_gui: true,
        cases_count: 0,
        casesListString: '',
        detectedInString: '',
        security_toolsString: '',
        esxi_version: '',
        os_version: '',
        additional_versions: '',
    },
  };
},
  computed: {
    filteredMachines() {
      let filtered = this.machines || [];
      if (this.filterType && this.filterType !== 'all') {
        filtered = filtered.filter(m => m.type === this.filterType);
      }
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        filtered = filtered.filter(m =>
          (m.name || '').toLowerCase().includes(q) ||
          (m.vuln_id || '').toLowerCase().includes(q) ||
          (m.status || '').toLowerCase().includes(q) ||
          (m.os || '').toLowerCase().includes(q)
        );
      }
      return filtered;
    }
  },
  methods: {
    addCase() {
    this.form.cases.push({ title: '', wiki_link: '' });
  },
    selectMachine(machine) {
      this.selectedMachineId = machine.id;
      this.$emit('select-machine', machine);
    },
    openAddModal() {
      this.showAddModal = true;
    },
    closeAddModal() {
      this.showAddModal = false;
      this.resetForm();
    },
    resetForm() {
      this.form = {
        name: '',
        vuln_id: '',
        type: 'ready',
        status: 'Используется',
        wiki_link: '',
        tagsString: '',
        description: '',
        writeupsString: '',
        os: 'Windows',
        has_gui: true,
        cases_count: 0,
        casesListString: '',
        detectedInString: '',
        security_toolsString: '',
        esxi_version: '',
        os_version: '',
        additional_versions: '',
      };
    },
    async submitForm() {
      // Валидация vuln_id
      const vulnIdPattern = /^Vuln-\d{3}$/;
      if (!vulnIdPattern.test(this.form.vuln_id)) {
        alert('ID уязвимости должен быть в формате Vuln-XXX (например: Vuln-001)');
        return;
      }

      // Валидация обязательных полей
      if (!this.form.name.trim()) {
        alert('Поле "Название" обязательно для заполнения');
        return;
      }
      if (!this.form.description.trim()) {
        alert('Поле "Описание" обязательно для заполнения');
        return;
      }
      if (!this.form.tagsString.trim()) {
        alert('Поле "Теги" обязательно для заполнения');
        return;
      }
      if (!this.form.detectedInString.trim()) {
        alert('Поле "В каких СЗИ детектируется" обязательно для заполнения');
        return;
      }
      if (!this.form.esxi_version.trim()) {
        alert('Поле "Версия ESXi" обязательно для заполнения');
        return;
      }
      if (!this.form.os_version.trim()) {
        alert('Поле "Версия ОС" обязательно для заполнения');
        return;
      }

      // Формируем payload
      const payload = {
        name: this.form.name,
        vuln_id: this.form.vuln_id,
        type: this.form.type,
        status: this.form.status,
        wiki_link: this.form.wiki_link || null,
        tags: this.form.tagsString ? this.form.tagsString.split(',').map(t => t.trim()).filter(Boolean).join(', ') : '',
        description: this.form.description,
        writeups: this.form.writeupsString || null,
        os: this.form.os,
        has_gui: this.form.has_gui,
        cases_count: this.form.cases_count,
        cases_list: this.form.casesListString || null,
        detected_in: this.form.detectedInString || '',
        security_tools: this.form.security_toolsString || '',
        esxi_version: this.form.esxi_version,
        os_version: this.form.os_version,
        additional_versions: this.form.additional_versions || null,
      };

      try {
        const response = await axios.post('http://localhost:8000/api/machines/', payload);
        
        // Локально добавляем новую машину в список
        const newMachine = response.data;
        this.machines.push(newMachine);
        
        this.closeAddModal();
        this.$emit('machine-added');
        // Убираем перезагрузку страницы, данные обновятся через событие
      } catch (error) {
        console.error('Ошибка при добавлении машины:', error);
        if (error.response && error.response.data) {
          console.error('Детали ошибки:', error.response.data);
          console.error('Отправленный payload:', payload);
          alert('Ошибка при добавлении машины: ' + JSON.stringify(error.response.data));
        } else {
          alert('Ошибка при добавлении машины');
        }
      }
    },
    async deleteMachine(id) {
      if (!confirm('Вы уверены?')) return;
      try {
        await axios.delete(`http://localhost:8000/api/machines/${id}/`);
        
        // Если удаляемая машина была выбрана, очищаем выбор
        if (this.selectedMachineId === id) {
          this.selectedMachineId = null;
          this.$emit('select-machine', null);
        }
        
        // Локально удаляем машину из списка
        const index = this.machines.findIndex(machine => machine.id === id);
        if (index !== -1) {
          this.machines.splice(index, 1);
        }
        
        this.$emit('machine-deleted');
      } catch (error) {
        alert('Ошибка при удалении');
        console.error(error);
      }
    }
  }
};

</script>

<style scoped>
/* Контейнер таблицы с машинами */
.table-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 15px;
  overflow: hidden;
}

/* Заголовок таблицы с названием и кнопкой */
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #999999;
  color: white;
  padding: 10px 15px;
  font-weight: 600;
  font-size: 1.1rem;
}

/* Кнопка добавления новой машины */
.add-button {
  background-color: #8aff00; /* кислотно-зеленый */
  border: none;
  padding: 6px 12px;
  border-radius: 15px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s ease;
}
.add-button:hover {
  background-color: #7bd600;
}

/* Таблица с машинами */
.machines-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #3c3c3c;
  flex-grow: 1;
  display: block;
  height: 100%; /* Высота для прокрутки */
  overflow-y: auto;
  color: white;
  overflow: hidden;
}

/* Заголовок таблицы */
.machines-table thead {
  display: table;
  width: 100%;
  table-layout: fixed;
  background-color: #ddd;
  color: #414141;
}

/* Тело таблицы с прокруткой */
.machines-table tbody {
  display: block;
  overflow-y: auto;
  height: 100%;
  width: 100%;
}

/* Строка таблицы */
.machines-table tr {
  display: table;
  width: 100%;
  table-layout: fixed;
  cursor: pointer;
}

/* Ячейки таблицы */
.machines-table th, .machines-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #ccc;
  vertical-align: middle;
}

/* Фиксация заголовков при прокрутке */
.machines-table th {
  position: sticky;
  top: 0;
  background-color: #ddd;
  z-index: 2;
}

/* Иконка ОС */
.os-icon {
  width: 24px;
  height: 24px;
}

/* Оверлей модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  overflow: hidden; /* Чтобы оверлей не прокручивался */
}

/* Содержимое модального окна */
.modal-content {
  background: #2f2f2f;
  padding: 30px 25px;
  border-radius: 10px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh; /* Ограничение по высоте */
  overflow-y: auto; /* Прокрутка содержимого */
  color: white;
  box-shadow: 0 0 15px rgba(0,0,0,0.5);
}

/* Заголовок модального окна */
.modal-content h3 {
  margin-bottom: 20px;
  text-align: center;
}

/* Метки в форме */
.modal-content form label {
  display: block;
  margin-top: 15px;
  font-weight: 600;
}

/* Стили для селектов */
.modal-content form select {
  width: 100%;
  padding: 8px 10px;
  margin-top: 5px;
  border-radius: 5px;
  border: none;
  font-size: 1rem;
  background-color: #444;
  color: white;
}

/* Стили для инпутов и textarea */
.modal-content form input,
.modal-content form textarea {
  width: 100%;
  padding: 8px 0px;
  margin-top: 5px;
  border-radius: 5px;
  border: none;
  font-size: 1rem;
  background-color: #444;
  color: white;
}

/* Контейнер кнопок в модальном окне */
.modal-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 25px;
  gap: 10px;
}

/* Стили для кнопок */
.modal-content form button,
.modal-buttons button {
  padding: 8px 16px;
  border-radius: 5px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* Кнопки отмены и закрытия */
.modal-content form button,
.modal-buttons button[type="button"] {
  margin-top: 5px;
  background-color: #555;
  color: white;
}
.modal-buttons button[type="button"]:hover {
  background-color: #777;
}

/* Кнопка подтверждения */
.modal-buttons button[type="submit"] {
  background-color: #8aff00;
  color: #222;
}
.modal-buttons button[type="submit"]:hover {
  background-color: #7bd600;
}
</style>
