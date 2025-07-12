<!--
v-if="machine" — показываем панель только если есть выбранная машина.

v-if="!isEditing" и v-else — переключение между просмотром и формой редактирования.

Методы startEditing, cancelEditing, saveChanges — управление режимом редактирования.

editForm — копия объекта для редактирования, чтобы не менять данные сразу.

watch на строки тегов, writeups и security_tools — синхронизация между строковым и массивным представлением.

Кнопки редактирования и удаления видны только для админа (isAdmin).
-->

<template>
  <!-- Панель подробной информации о машине -->
  <aside class="details-panel" v-if="machine">
    <div class="header-gradient">
      <!-- Название машины -->
      <h3 class="machine-name">{{ machine.name }}</h3>

      <!-- Блок действий (редактировать, удалить) виден только для админа или автора -->
      <div class="actions" v-if="canEditOrDelete">
        <!-- Кнопка редактирования видна, если не в режиме редактирования -->
        <button v-if="!isEditing" class="edit-btn" title="Редактировать" @click="startEditing">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 20h9" />
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4 12.5-12.5z" />
          </svg>
        </button>
        <!-- Кнопка удаления  -->
        <button v-if="!isEditing" class="delete-btn" title="Удалить" @click="deleteMachine">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
        <!-- Кнопки сохранения, отмены и удаления видны в режиме редактирования -->
        <div v-else>
          <button class="save-btn" title="Сохранить" @click="saveChanges">Сохранить</button>
          <button class="cancel-btn" title="Отмена" @click="cancelEditing">Отмена</button>
          <button class="delete-btn" title="Удалить" @click="deleteMachine">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Отображение информации в режиме просмотра -->
    <div class="details-content" v-if="!isEditing">
      <p><strong>ID:</strong> {{ machine.vuln_id }}</p>
      <p><strong>Название:</strong> {{ machine.name }}</p>
      <p><strong>Тип:</strong> {{ machine.type === 'ready' ? 'Готовая' : 'Идея' }}</p>
      <p><strong>Статус:</strong> {{ machine.status }}</p>
      <p><strong>Ссылка на Wiki:</strong> {{ machine.wiki_link || 'Не указана' }}</p>
      <p>
        <strong>Теги:</strong>
        <span v-for="tag in tagsArray" :key="tag" class="tag">{{ tag }}</span>
      </p>
      <p><strong>Описание:</strong> {{ machine.description }}</p>
      <p><strong>WriteUp'ы:</strong> {{ writeupsArray.join(', ') || 'Не указаны' }}</p>
      <p><strong>ОС:</strong> {{ machine.os }}</p>
      <p><strong>Графика в ОС:</strong> {{ machine.has_gui ? 'Да' : 'Нет' }}</p>
      <p><strong>Количество кейсов:</strong> {{ machine.cases_count }}</p>
      <p><strong>Список кейсов:</strong> {{ casesListArray.join(', ') || 'Не указаны' }}</p>
      <p><strong>В каких СЗИ детектируется:</strong> {{ machine.detected_in }}</p>
      <p><strong>Средства защиты:</strong> {{ machine.security_tools }}</p>
      <p><strong>Версия ESXi:</strong> {{ machine.esxi_version }}</p>
      <p><strong>Версия ОС:</strong> {{ machine.os_version }}</p>
      <p><strong>Дополнительные версии ПО:</strong> {{ machine.additional_versions || 'Нет' }}</p>
      <p><strong>Создатель:</strong> {{ machine.creator }}</p>
      <p><strong>Дата создания:</strong> {{ new Date(machine.created_at).toLocaleDateString() }}</p>
      <p><strong>Дата обновления:</strong> {{ new Date(machine.updated_at).toLocaleDateString() }}</p>
    </div>

    <!-- Форма редактирования, отображается, если isEditing = true -->
    <div class="details-content" v-else>
      <label>ID:</label>
      <input v-model="editForm.vuln_id" type="text" />

      <label>Название:</label>
      <input v-model="editForm.name" type="text" />

      <label>Тип:</label>
      <select v-model="editForm.type">
        <option value="ready">Готовая</option>
        <option value="idea">Идея</option>
      </select>

      <label>Статус:</label>
      <select v-model="editForm.status">
        <option value="Используется">Используется</option>
        <option value="Не используется">Не используется</option>
      </select>

      <label>Ссылка на Wiki:</label>
      <input v-model="editForm.wiki_link" type="url" />

      <label>Теги (через запятую):</label>
      <input v-model="editForm.tagsString" type="text" />

      <label>Описание:</label>
      <textarea v-model="editForm.description"></textarea>

      <label>WriteUp'ы (через запятую):</label>
      <input v-model="editForm.writeupsString" type="text" />

      <label>ОС:</label>
      <select v-model="editForm.os">
        <option value="Windows">Windows</option>
        <option value="Linux">Linux</option>
        <option value="Android">Android</option>
        <option value="MacOS">MacOS</option>
      </select>

      <label>Графика в ОС:</label>
      <select v-model="editForm.has_gui">
        <option :value="true">Да</option>
        <option :value="false">Нет</option>
      </select>

      <label>Количество кейсов:</label>
      <input v-model.number="editForm.cases_count" type="number" min="0" />

      <label>Список кейсов (через запятую):</label>
      <input v-model="editForm.casesListString" type="text" />

      <label>В каких СЗИ детектируется (через запятую):</label>
      <input v-model="editForm.detectedInString" type="text" />

      <label>Средства защиты (через запятую):</label>
      <input v-model="editForm.security_tools" type="text" />

      <label>Версия ESXi:</label>
      <input v-model="editForm.esxi_version" type="text" />

      <label>Версия ОС:</label>
      <input v-model="editForm.os_version" type="text" />

      <label for="additional_versions">Дополнительные версии ПО</label>
      <textarea v-model="editForm.additional_versions"></textarea>

      <div class="form-group">
        <label>Создатель:</label>
        <input v-model="editForm.creator" type="text" readonly />
      </div>
    </div>
  </aside>

  <!-- Если машина не выбрана, показываем заглушку -->
  <aside v-else class="details-panel empty">
    <p>Выберите машину для просмотра деталей</p>
  </aside>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DetailsPanel',
  props: {
    machine: {
      type: Object,
      required: false,
      default: null,
    },
    isAdmin: {
      type: Boolean,
      default: true,
    },
    currentUser: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      isEditing: false,
      editForm: null,
    };
  },
  computed: {
    canEditOrDelete() {
      if (!this.machine) return false;
      // Проверяем, является ли пользователь админом или автором машины
      return this.isAdmin || (this.machine.creator === this.currentUser);
    },
    tagsArray() {
      if (!this.machine || !this.machine.tags) return [];
      if (Array.isArray(this.machine.tags)) return this.machine.tags;
      if (typeof this.machine.tags === 'string') {
        return this.machine.tags.split(',').map(s => s.trim()).filter(s => s);
      }
      return [];
    },
    writeupsArray() {
      if (!this.machine || !this.machine.writeups) return [];
      if (Array.isArray(this.machine.writeups)) return this.machine.writeups;
      if (typeof this.machine.writeups === 'string') {
        return this.machine.writeups.split(',').map(s => s.trim()).filter(s => s);
      }
      return [];
    },
    detectedInArray() {
      if (!this.machine || !this.machine.detected_in) return [];
      if (Array.isArray(this.machine.detected_in)) return this.machine.detected_in;
      if (typeof this.machine.detected_in === 'string') {
        return this.machine.detected_in.split(',').map(s => s.trim()).filter(s => s);
      }
      return [];
    },
    casesListArray() {
      if (!this.machine || !this.machine.cases_list) return [];
      if (Array.isArray(this.machine.cases_list)) return this.machine.cases_list;
      if (typeof this.machine.cases_list === 'string') {
        return this.machine.cases_list.split(',').map(s => s.trim()).filter(s => s);
      }
      return [];
    },
  },
  methods: {
    startEditing() {
      this.isEditing = true;
      this.editForm = JSON.parse(JSON.stringify(this.machine));
      
      // Преобразуем is_used в статус для отображения
      this.editForm.status = this.machine.is_used ? 'Используется' : 'Не используется';
      
      // Инициализация строковых полей для удобного редактирования
      this.editForm.tagsString = this.tagsArray.join(', ');
      this.editForm.writeupsString = this.writeupsArray.join(', ');
      this.editForm.detectedInString = this.detectedInArray.join(', ');
      this.editForm.casesListString = this.casesListArray.join(', ');
    },
    cancelEditing() {
      this.isEditing = false;
      this.editForm = null;
    },
    async saveChanges() {
      try {
        // Отправляем все поля, которые есть в модели Django
        const payload = {
          name: this.editForm.name,
          vuln_id: this.editForm.vuln_id,
          wiki_link: this.editForm.wiki_link || null,
          tags: this.editForm.tagsString ? this.editForm.tagsString.split(',').map(s => s.trim()).filter(s => s).join(', ') : '',
          description: this.editForm.description,
          writeups: this.editForm.writeupsString || null,
          os: this.editForm.os,
          has_gui: this.editForm.has_gui,
          cases_count: this.editForm.cases_count,
          cases_list: this.editForm.casesListString || null,
          detected_in: this.editForm.detectedInString || '',
          esxi_version: this.editForm.esxi_version,
          os_version: this.editForm.os_version,
          additional_versions: this.editForm.additional_versions || null,
          type: this.editForm.type,
          status: this.editForm.status,
          security_tools: this.editForm.security_tools || null,
        };

        const response = await axios.patch(`http://localhost:8000/api/machines/${this.editForm.id}/`, payload);
        
        // Обновляем данные машины сразу после сохранения
        Object.assign(this.machine, response.data);
        
        this.$emit('update-machine', this.machine);
        this.isEditing = false;
        this.editForm = null;
      } catch (error) {
        console.error('Ошибка при сохранении изменений:', error);
        if (error.response && error.response.data) {
          console.error('Детали ошибки:', error.response.data);
          console.error('Отправленный payload:', payload);
          alert('Ошибка при сохранении: ' + JSON.stringify(error.response.data));
        } else {
          alert('Не удалось сохранить изменения.');
        }
      }
    },
    async deleteMachine() {
      if (!confirm('Вы уверены, что хотите удалить эту машину?')) return;

      try {
        await axios.delete(`http://localhost:8000/api/machines/${this.machine.id}/`);
        this.$emit('machine-deleted', this.machine.id);
      } catch (error) {
        console.error('Ошибка при удалении:', error);
        alert('Не удалось удалить машину.');
      }
    },
  },
};
</script>

<style scoped>
/* Стили для панели подробной информации */
.details-panel {
  box-sizing: border-box;
  height: 90vh; /* ограничение по высоте для прокрутки */
  position: sticky;
  top: 0;
  overflow-y: auto;

  background-color: #141414;
  border-radius: 15px;
  color: white;

  padding: 2%;
  margin: 1%;
}

/* Заголовок с градиентом и кнопками */
.header-gradient {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(90deg, #ff9abc, #ff7e5f);
  padding: 10px 15px;
  border-radius: 15px;
  margin-bottom: 15px;
}

/* Название машины */
.machine-name {
  margin: 0;
  color: white;
  font-weight: 700;
  font-size: 1.2rem;
}

/* Кнопки действий */
.actions button {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  margin-left: 10px;
}

/* Стили для тегов */
.tag {
  display: inline-block;
  background-color: #555;
  padding: 3px 8px;
  margin-right: 5px;
  border-radius: 15px;
  font-size: 0.85rem;
}

/* Контейнер с деталями */
.details-content {
  padding-top: 1%;
}

/* Отступы для абзацев */
.details-content p {
  margin: 8px 0;
}

/* Списки */
.details-content ul {
  padding-left: 20px;
  margin: 4px 0;
}

/* Ссылки */
.details-content a {
  color: #8aff00;
  text-decoration: none;
}

.details-content a:hover {
  text-decoration: underline;
}

.details-content[v-cloak][v-if="isEditing"] {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.details-content label {
  font-weight: 600;
  margin-bottom: 10px;
  color: #ccc;
}

.details-content input,
.details-content select,
.details-content textarea {
  padding: 6px 10px;
  border-radius: 6px;
  border: none;
  background-color: #222;
  color: white;
  font-size: 1rem;
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
}

.case-item {
  display: flex;
  gap: 10px;
  margin-bottom: 8px;
}

.case-item input {
  flex: 1;
}

.case-item button {
    background-color: #b0b0b0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  padding: 4px 8px;
  color: #222;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.case-item button:hover {
    background-color: #808080;
}

.actions-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* Общие стили для кнопок добавления */
.add-case-button,
.add-version-button {
    background-color: #8aff00;
  margin: 5px;
  margin-bottom: 10px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  padding: 6px 12px;
  color: #222;
  font-weight: 600;
  transition: background-color 0.3s ease;
  display: inline-block;
}

.add-case-button:hover,
.add-version-button:hover {
    background-color: #7bd600;
}

</style>
