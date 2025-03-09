# Реализация фронтэнда на основе 3 лабораторной работы

###  Настройка CORS в Django REST framework

Установка django-cors-headers:

    pip install django-cors-headers


Затем обновляем settings.py:  

    INSTALLED_APPS = (
        ##...
        'corsheaders'
    )

HTTP-запросы отправляем на сервер с помощью библиотеки axios. 

```python
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/', 
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;
```

### Реализация интерфейсов .vue

Под тэгом <template> указан шаблон элементов страницы.

Под тэгом <script> приведены функции и методы, которые необходимо вызвать в различных кейсах (при загрузке страницы, при нажатии на определенную кнопку и т.д.)

Под тэгом <style> перечислены стили элементов.

Для примера:

Crews.vue - список всех экипажей.

```vue
<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Crews list</h1>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" md="6">
          <v-select
            v-model="filters.employee"
            :items="employeeChoices"
            label="Search by employee"
            item-value="id"
            item-title="name"
            clearable
          ></v-select>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col
          cols="12"
          md="6"
          v-for="crew in paginatedCrews"
          :key="crew.id"
        >
          <v-card class="mb-6" elevation="2">
            <v-card-title>
              Crew {{ crew.id }}
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <p><strong>Captain:</strong> {{ crew.captain.employee.first_name }} {{ crew.captain.employee.last_name }} ({{ crew.captain.employee.work_experience_years }} years of exp)</p>
              <v-divider class="my-2"></v-divider>
              <p><strong>Co-pilot:</strong> {{ crew.co_pilot.employee.first_name }} {{ crew.co_pilot.employee.last_name }} ({{ crew.co_pilot.employee.work_experience_years }} years of exp)</p>
              <v-divider class="my-2"></v-divider>
              <p><strong>Navigator:</strong> {{ crew.navigator.employee.first_name }} {{ crew.navigator.employee.last_name }} ({{ crew.navigator.employee.work_experience_years }} years of exp)</p>
              <v-divider class="my-2"></v-divider>
              <p><strong>Stewards:</strong></p>
              <ul class="stops-list">
                <li
                  v-for="attendant in crew.attendants"
                  :key="attendant.employee.first_name + attendant.employee.last_name"
                >
                  {{ attendant.employee.first_name }} {{ attendant.employee.last_name }} ({{ attendant.employee.work_experience_years }} years of exp)
                </li>
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" class="d-flex justify-center">
          <v-pagination
            v-model="currentPage"
            :length="totalPages"
            :total-visible="5"
          ></v-pagination>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    data() {
      return {
        crews: [],
        filters: {
          employee: null,
        },
        employeeChoices: [],
        currentPage: 1,
        itemsPerPage: 6,
      };
    },
    computed: {
      filteredCrews() {
        if (!this.filters.employee) {
          return this.crews;
        }
  
        return this.crews.filter((crew) =>
          [crew.captain, crew.co_pilot, crew.navigator, ...crew.attendants]
            .map((member) => member.employee.id)
            .includes(this.filters.employee)
        );
    
      },
      paginatedCrews() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.filteredCrews.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.filteredCrews.length / this.itemsPerPage);
      },
    },
    methods: {
      async fetchCrews() {
        try {
          const response = await apiClient.get("/crews/");
          this.crews = response.data;
        } catch (error) {
          console.error("Crews loading error:", error.response?.data || error.message);
          alert("Crews loading error.");
        }
      },
      async fetchEmployees() {
        try {
          const response = await apiClient.get("/employees/");
          this.employeeChoices = response.data.map((employee) => ({
            id: employee.id,
            name: `${employee.first_name} ${employee.last_name}`,
          }));
        } catch (error) {
          console.error("Employee list loading error:", error.response?.data || error.message);
          alert("Employee list loading error.");
        }
      },
    },
    async created() {
      await Promise.all([this.fetchCrews(), this.fetchEmployees()]);
    },
  };
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  .v-card-title {
    font-weight: bold;
  }
  .v-card-text p {
    margin: 4px 0;
  }
  
  
  </style>
```
