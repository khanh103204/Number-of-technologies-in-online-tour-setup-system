<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <h2>🛠 Admin Panel</h2>
      <ul>
        <li><router-link to="/admin/dashboard">Dashboard</router-link></li>
        <li><router-link to="/admin/tours">Quản lý tour</router-link></li>
        <li><router-link to="/admin/users">Người dùng</router-link></li>
        <li><router-link to="/admin/settings">Cài đặt</router-link></li>
      </ul>
    </aside>

    <main class="admin-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f4f6f8;
}
.sidebar {
  width: 220px;
  background: #1976d2;
  color: white;
  padding: 1.5rem;
}
.sidebar h2 { margin-bottom: 1rem; font-size: 1.2rem; }
.sidebar ul { list-style: none; padding: 0; }
.sidebar li { margin: 0.8rem 0; }
.sidebar a {
  color: white;
  text-decoration: none;
  font-weight: 500;
}
.sidebar a.router-link-active { text-decoration: underline; }
.admin-content {
  flex: 1;
  padding: 2rem;
}
</style>
