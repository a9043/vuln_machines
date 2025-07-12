<template>
  <div class="login-page">
    <!-- Форма логина/регистрации с обработчиком отправки onSubmit -->
    <form class="login-form" @submit.prevent="onSubmit">
      <!-- Заголовок меняется в зависимости от режима (регистрация или вход) -->
      <h2>{{ isRegistering ? 'Регистрация' : 'Вход в систему' }}</h2>

      <label for="username">Имя пользователя</label>
      <input id="username" v-model="username" type="text" required />

      <label for="password">Пароль</label>
      <input id="password" v-model="password" type="password" required />

      <!-- Поле подтверждения пароля показывается только в режиме регистрации -->
      <label v-if="isRegistering" for="confirmPassword">Подтвердите пароль</label>
      <input
        v-if="isRegistering"
        id="confirmPassword"
        v-model="confirmPassword"
        type="password"
        required
      />

      <!-- Выбор типа пользователя только при регистрации -->
      <label v-if="isRegistering" for="userType">Тип пользователя</label>
      <select v-if="isRegistering" id="userType" v-model="userType" required>
        <option value="user">Обычный пользователь</option>
        <option value="admin">Администратор</option>
      </select>

      <!-- Кнопка отправки формы с текстом в зависимости от режима -->
      <button type="submit" class="submit-button">
        {{ isRegistering ? 'Зарегистрироваться' : 'Войти' }}
      </button>

      <!-- Кнопка переключения между режимами регистрации и входа -->
      <button type="button" class="toggle-button" @click="toggleForm">
        {{ isRegistering ? 'Уже есть аккаунт? Войти' : 'Нет аккаунта? Зарегистрироваться' }}
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      isRegistering: false,
      username: '',
      password: '',
      confirmPassword: '',
      userType: 'user', // По умолчанию обычный пользователь
    };
  },
  methods: {
    toggleForm() {
      this.isRegistering = !this.isRegistering;
      this.username = '';
      this.password = '';
      this.confirmPassword = '';
      this.userType = 'user';
    },
    async onSubmit() {
      if (this.isRegistering) {
        if (this.password !== this.confirmPassword) {
          alert('Пароли не совпадают!');
          return;
        }
        try {
          await axios.post('/register/', {
            username: this.username,
            password: this.password,
            user_type: this.userType,
          });
          // После успешной регистрации сразу логинимся
          await this.loginUser();
        } catch (error) {
          alert('Ошибка регистрации: ' + (error.response?.data?.username || error.message));
        }
      } else {
        await this.loginUser();
      }
    },
    async loginUser() {
      try {
        const response = await axios.post('/token/', {
          username: this.username,
          password: this.password,
        });
        const token = response.data.access;
        // Получаем инфо о пользователе
        const userInfo = await axios.get('/users/me/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        localStorage.setItem('token', token);
        localStorage.setItem('username', userInfo.data.username);
        localStorage.setItem('isAdmin', userInfo.data.is_staff);
        this.$router.push({ name: 'Home' });
        window.location.reload();
      } catch (error) {
        alert('Ошибка входа: ' + (error.response?.data?.detail || error.message));
      }
    },
  },
};
</script>

<style scoped>
/* Контейнер страницы логина/регистрации центрирует форму по вертикали и горизонтали */
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Высота на весь экран */
  background-color: #2f2f2f; /* Темный фон */
}

/* Стили формы */
.login-form {
  background: white;
  padding: 5px 40px 40px 40px;
  border-radius: 8px;
  width: 320px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
}

/* Заголовок формы */
.login-form h2 {
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

/* Стили для меток */
.login-form label {
  margin-bottom: 6px;
  font-weight: 600;
  color: #555;
}

/* Стили для полей ввода */
.login-form input,
.login-form select {
  padding: 8px 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

/* Стили для селекта */
.login-form select {
  background-color: white;
  cursor: pointer;
}

/* Кнопка отправки формы */
.submit-button {
  background-color: #8aff00;
  border: none;
  padding: 10px;
  font-weight: 700;
  color: #222;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

/* Эффект при наведении на кнопку отправки */
.submit-button:hover {
  background-color: #7bd600;
}

/* Кнопка переключения между режимами */
.toggle-button {
  margin-top: 5px;
  background-color: #c3c3c3;
  border: none;
  padding: 10px;
  font-weight: 700;
  color: #222;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

/* Эффект при наведении на кнопку переключения */
.toggle-button:hover {
  background-color: #e5e5e5;
}
</style>
