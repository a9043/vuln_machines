<template>
  <header class="header">
    <div class="left">
      <span v-if="!username" class="login-text" @click="goToLogin">Вход</span>
      <!-- Иконка замка -->
      <svg class="lock-icon" viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
        <path d="M12 17a2 2 0 1 0 0-4 2 2 0 0 0 0 4zm6-7h-1V7a5 5 0 0 0-10 0v3H6a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2zM8 7a4 4 0 0 1 8 0v3H8V7z"/>
      </svg>
    </div>
    <div class="right">
      <span class="username" v-if="username">
        {{ username }}
        <span class="user-type">
          {{ isAdmin ? '(Админ)' : '(Пользователь)' }}
        </span>
      </span>
      <img class="avatar" src="@/assets/default-avatar.png" alt="User Avatar" />
      <button v-if="username" class="logout-btn" @click="logout">Выйти</button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderApp',
  props: {
    username: String,
    isAdmin: Boolean,
  },
  methods: {
    // Метод для перехода на страницу логина
    goToLogin() {
      this.$router.push({ name: 'Login' });
    },
    logout() {
      localStorage.clear();
      this.$router.push({ name: 'Login' });
      window.location.reload();
    },
  },
};
</script>


<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgb(255, 255, 255);
  padding: 0.5% 1%;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

.left, .right {
  display: flex;
  align-items: center;
}

.login-text {
  margin-right: 8px;
  font-weight: 600;
  color: #333;
  cursor: pointer;
}

.lock-icon {
  color: #666;
}

.username {
  margin-right: 10px;
  font-weight: 600;
  color: #333;
}

.user-type {
  font-size: 0.9em;
  font-weight: 400;
  margin-left: 5px;
  color: #333;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  background-color: #ccc;
}

.logout-btn {
  margin-left: 10px;
  background: #ff7e5f;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-weight: 600;
  cursor: pointer;
}
.logout-btn:hover {
  background: #ff9abc;
}
</style>
