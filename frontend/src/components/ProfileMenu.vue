<!-- eslint-disable prettier/prettier -->
<!-- eslint-disable prettier/prettier -->
<script>
import { useAuthStore } from '../store/auth.js';
import { useRouter } from 'vue-router';

export default {
    name: 'ProfileMenu',
    data() {
        return {
            user: {
                name: '',
                email: '',
                avatar: 'https://primefaces.org/cdn/primevue/images/avatar/ionibowcher.png'
            },
            authStore: useAuthStore(),
            router: useRouter(),
            items: [
                {
                    header: true
                },
                {
                    label: 'Profile',
                    icon: 'pi pi-user',
                    to: '/profile'
                },
                {
                    label: 'Settings',
                    icon: 'pi pi-cog',
                    to: '/settings'
                },
                {
                    separator: true
                },
                {
                    label: 'Logout',
                    icon: 'pi pi-power-off',
                    command: () => this.handleLogout()
                }
            ]
        }
    },
    methods: {
        toggleMenu(event) {
            this.$refs.menu.toggle(event);
        },
        async handleLogout() {
            try {
                await this.authStore.logout(this.router);
            } catch (error) {
                console.error('Logout error:', error);
            }
        }
    },
    async mounted() {
        await this.authStore.fetchUser();
        this.user.name = this.authStore.user.username?.split('@')[0] || '';
        this.user.email = this.authStore.user.email;
    }
}
</script>
<template>
    <div class="profile-menu">
        <Button type="button" class="layout-topbar-action p-link" @click="toggleMenu" aria-haspopup="true"
            aria-label="Profile">
            <i class="pi pi-user"></i>
            <span>Profile</span>
        </Button>

        <Menu ref="menu" :model="items" :popup="true" class="profile-menu-list">
            <template #item="{ item }">
                <div v-if="item.header" class="profile-header p-12">
                    <img :src="user.avatar" :alt="user.name" class="profile-image mb-2"
                        style="width: 100px; height: 100px; border-radius: 50%" />
                    <div class="font-bold">{{ user.name }}</div>
                    <div class="text-sm text-gray-600">{{ user.email }}</div>
                </div>
                <router-link v-else-if="item.to" :to="item.to" class="p-menuitem-link">
                    <i :class="item.icon" class="mr-2"></i>
                    <span>{{ item.label }}</span>
                </router-link>
                <a v-else @click="item.command" class="p-menuitem-link">
                    <i :class="item.icon" class="mr-2"></i>
                    <span>{{ item.label }}</span>
                </a>
            </template>
        </Menu>
    </div>
</template>

<style scoped>
.profile-menu {
    position: relative;
}

.profile-menu-list {
    min-width: 200px;
}

.profile-header {
    text-align: center;
}

.p-menuitem-link {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    color: var(--text-color);
    cursor: pointer;
    text-decoration: none;
}

.p-menuitem-link:hover {
    background-color: var(--surface-hover);
}

.layout-topbar-action {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    position: relative;
    padding: 0.5rem;
}

.layout-topbar-action:hover {
    background-color: var(--surface-hover);
}
</style>
