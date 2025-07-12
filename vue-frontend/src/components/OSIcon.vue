<!--
Проп os — принимает только заранее определённые значения, что предотвращает ошибки.

Вычисляемое свойство letter — возвращает первую букву ОС для отображения в иконке.

Вычисляемое свойство osClass — используется для динамического добавления CSS-класса, чтобы стилизовать иконку под конкретную ОС.
-->

<template>
  <!-- Контейнер иконки ОС с динамическим классом для стилизации -->
  <div class="os-icon" :class="osClass">
    <!-- Отображаемая буква, зависящая от типа ОС -->
    {{ letter }}
  </div>
</template>

<script>
export default {
  name: 'OSIcon',
  props: {
    // Проп os — строка, обязательна, принимает только определённые значения
    os: {
      type: String,
      required: true,
      validator: value => ['Linux', 'Windows', 'MacOS', 'Android'].includes(value),
      // Проверка, что значение пропа входит в список поддерживаемых ОС
    },
  },
  computed: {
    // Вычисляемая буква для отображения в иконке в зависимости от ОС
    letter() {
      switch (this.os) {
        case 'Linux': return 'L';
        case 'Windows': return 'W';
        case 'MacOS': return 'M';
        case 'Android': return 'A';
        default: return '?'; // На случай неизвестной ОС
      }
    },
    // Класс CSS для стилизации иконки, например 'linux', 'windows' и т.д.
    osClass() {
      return this.os.toLowerCase();
    },
  },
};
</script>

<style scoped>
.os-icon {
  width: 24px;
  height: 24px;
  font-weight: 700;
  font-size: 20px;
  line-height: 24px;
  text-align: center;
  color: #a3a3a3;
  font-family: 'Georgia', 'Times New Roman', serif;
  text-shadow:
    1px 1px 0 #000000;
  user-select: none;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

</style>
