<template>
  <div id="app">
    <HeaderApp :username="username" :is-admin="isAdmin" />
     
    <!--
    <LoginPage />
  -->

    <div class="layout">
      <FiltersPanel />
      <MainContent
        ref="mainContent"
        :selectedView="selectedView"
        :searchQuery="searchQuery"
        @select-machine="onSelectMachine"
        @machine-deleted="onMachineDeleted"
      />
    <DetailsPanel 
      :machine="selectedMachine" 
      :is-admin="isAdmin" 
      :current-user="username"
      @machine-deleted="onMachineDeleted"
    />
    </div>
  </div>
</template>

<script>
import LoginPage from './components/LoginPage.vue';
import HeaderApp from './components/HeaderApp.vue';
import FiltersPanel from './components/FiltersPanel.vue';
import MainContent from './components/MainContent.vue';
import DetailsPanel from './components/DetailsPanel.vue';

export default {
  name: 'App',
  components: {
    HeaderApp,
    FiltersPanel,
    MainContent,
    DetailsPanel,
    LoginPage,
  },
  data() {
    return {
      selectedView: 'all',
      searchQuery: '',
      selectedMachine: null,
      isAdmin: localStorage.getItem('isAdmin') === 'true',
      username: localStorage.getItem('username') || '',
    };
  },
  methods: {
    onSelectMachine(machine) {
      this.selectedMachine = machine;
    },
    onMachineDeleted() {
      this.selectedMachine = null;
      // Обновляем данные в MainContent
      if (this.$refs.mainContent) {
        this.$refs.mainContent.fetchMachines();
      }
    },
  },
};
</script>

<style>

#app {
  display: flex;
  flex-direction: column;
}

body, #app {
  font-family: 'Bahnschrift', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #000000; /* чёрный фон */
  margin: 0;
  padding: 0;
  height: 100%;
   overflow: hidden;
}

.layout {
  flex: 1;
  display: flex;
}

.filters-panel {
  width: 20%;
}

.main-content {
  width: 65%;
        height: 90vh; /* ограничиваем высоту, например 90% высоты окна */

}

.details-panel {
  width: 25%;
}
</style>