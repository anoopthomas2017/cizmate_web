<template>
    <Fluid>
        <Toast />
        <ConfirmDialog />

        <div class="flex flex-col md:flex-row gap-8">
            <div class="md:w-1/2">
                <div class="card flex flex-col gap-4">
                    <div class="font-semibold text-xl">
                        {{ editing ? 'Edit Category' : 'Create Category' }}
                    </div>

                    <div class="flex flex-col gap-2">
                        <label for="name">Name</label>
                        <InputText id="name" v-model="form.name" :class="{ 'p-invalid': errors.name }" />
                        <small class="p-error" v-if="errors.name">{{ errors.name }}</small>
                    </div>

                    <div class="flex flex-col gap-2">
                        <label for="description">Description</label>
                        <Textarea id="description" v-model="form.description" rows="4" autoResize />
                    </div>

                    <div class="flex items-center gap-2">
                        <Checkbox id="is_active" v-model="form.is_active" :binary="true" />
                        <label for="is_active">Active</label>
                    </div>

                    <div class="flex gap-2">
                        <Button @click="saveCategory" :label="editing ? 'Update' : 'Create'" :loading="loading" />
                        <Button v-if="editing" @click="cancelEdit" label="Cancel" severity="secondary" />
                    </div>
                </div>
            </div>

            <div class="md:w-1/2">
                <div class="card">
                    <div class="font-semibold text-xl mb-4">Categories List</div>
                    <DataTable :value="formattedCategories" :loading="loading" :paginator="true" :rows="10"
                        responsiveLayout="scroll">
                        <Column field="name" header="Name" sortable></Column>
                        <Column field="description" header="Description"></Column>
                        <Column field="is_active" header="Status" sortable>
                            <template #body="slotProps">
                                <Tag :severity="slotProps.data.is_active ? 'success' : 'danger'">
                                    {{ slotProps.data.is_active ? 'Active' : 'Inactive' }}
                                </Tag>
                            </template>
                        </Column>
                        <Column header="Actions">
                            <template #body="slotProps">
                                <div class="flex gap-2">
                                    <Button icon="pi pi-pencil" @click="editCategory(slotProps.data)" severity="info"
                                        text />
                                    <Button icon="pi pi-trash" @click="confirmDelete(slotProps.data)" severity="danger"
                                        text />
                                </div>
                            </template>
                        </Column>
                    </DataTable>
                </div>
            </div>
        </div>
    </Fluid>
</template>

<script>
import { mapState, mapActions } from 'pinia';
import { useCategoryStore } from '../../../store/categoryStore';

export default {
    name: 'Categories',
    data() {
        return {
            form: {
                name: '',
                description: '',
                is_active: true,
                parent: ''

            },
            editing: false,
            errors: {}
        };
    },
    computed: {
        ...mapState(useCategoryStore, ['categories', 'loading', 'error']),
        formattedCategories() {
            return this.categories.map(category => ({
                id: category.id,
                name: category.name,
                description: category.description,
                is_active: category.is_active,
                created_at: category.created_at
            }));
        }
    },
    methods: {
        ...mapActions(useCategoryStore, [
            'fetchCategories',
            'createCategory',
            'updateCategory',
            'deleteCategory'
        ]),
        async saveCategory() {
            this.errors = {};
            try {
                if (this.editing) {
                    await this.updateCategory(this.form.id, this.form);
                } else {
                    await this.createCategory(this.form);
                }
                this.resetForm();
            } catch (error) {
                if (error.response?.data?.errors) {
                    this.errors = error.response.data.errors;
                }
            }
        },
        editCategory(category) {
            this.form = { ...category };
            this.editing = true;
        },
        async confirmDelete(category) {
            try {
                await this.$confirm.require({
                    message: 'Are you sure you want to delete this category?',
                    header: 'Delete Confirmation',
                    icon: 'pi pi-exclamation-triangle',
                    acceptClass: 'p-button-danger',
                    accept: async () => {
                        try {
                            await this.deleteCategory(category.id);
                            this.$toast.add({
                                severity: 'success',
                                summary: 'Success',
                                detail: 'Category deleted successfully',
                                life: 3000
                            });
                            await this.fetchCategories(); // Refresh the list
                        } catch (error) {
                            this.$toast.add({
                                severity: 'error',
                                summary: 'Error',
                                detail: 'Failed to delete category',
                                life: 3000
                            });
                        }
                    }
                });
            } catch (error) {
                console.error('Delete confirmation error:', error);
            }
        },
        async removeCategory(id) {
            try {
                this.$confirm.require({
                    message: 'Are you sure you want to delete this category?',
                    header: 'Confirm Delete',
                    icon: 'pi pi-exclamation-triangle',
                    accept: async () => {
                        await this.deleteCategory(id);
                        this.$toast.add({
                            severity: 'success',
                            summary: 'Success',
                            detail: 'Category deleted successfully',
                            life: 3000
                        });
                    }
                });
            } catch (error) {
                this.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Failed to delete category',
                    life: 3000
                });
            }
        },
        cancelEdit() {
            this.resetForm();
        },
        resetForm() {
            this.form = {
                name: '',
                description: '',
                is_active: true,
                parent: ''
            };
            this.editing = false;
            this.errors = {};
        }
    },
    created() {
        this.fetchCategories();
    }
};
</script>

<style scoped>
.card {
    padding: 1.5rem;
    border-radius: 6px;
    background: var(--surface-card);
}
</style>
