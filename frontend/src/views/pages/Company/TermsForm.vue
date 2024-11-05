<!-- src/components/TermsCrud.vue -->
<template>
    <div class="card">
        <Toast />

        <div class="header-section mb-4">
            <h2>Terms Management</h2>
            <div class="button-group" v-if="terms.length">
                <Button icon="pi pi-pencil" class="p-button-text p-button-sm" @click="editTerm(terms[0])" />
                <Button icon="pi pi-trash" class="p-button-text p-button-sm p-button-danger"
                    @click="confirmDelete(terms[0])" />
            </div>
            <Button v-else label="Add New Terms" icon="pi pi-plus" @click="openNew" />
        </div>

        <div v-if="terms.length" class="terms-container">
            <div v-for="(value, key) in getTermFields(terms[0])" :key="key" class="term-item">
                <div class="term-header">
                    <h3>Term {{ key.replace('term', '') }}</h3>
                </div>
                <p class="term-content">{{ value || 'No content' }}</p>
            </div>
        </div>

        <div v-else class="empty-state">
            <i class="pi pi-file mb-3" style="font-size: 2rem"></i>
            <p>No terms have been added yet</p>
        </div>

        <Dialog v-model:visible="termDialog" :style="{ width: '450px' }"
            :header="dialogMode === 'create' ? 'Add New Terms' : 'Edit Terms'" :modal="true" class="p-fluid">
            <div v-for="i in 5" :key="i" class="field mb-4">
                <label :for="'term' + i" class="block mb-2">Term {{ i }}</label>
                <Textarea :id="'term' + i" v-model="term['term' + i]" required="false" rows="3" cols="20" />
            </div>

            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" class="p-button-text" :loading="saveLoading"
                    @click="saveTerm" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteTermDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="confirmation-content">
                <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
                <span>Are you sure you want to delete the selected Terms?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" class="p-button-text" @click="deleteTermDialog = false" />
                <Button label="Yes" icon="pi pi-check" class="p-button-text" @click="confirmDeleteTerm" />
            </template>
        </Dialog>
    </div>
</template>

<script>
import { useCompanyInfoStore } from '../../../store/companyInfo';
import { useTermsStore } from '../../../store/terms'

export default {
    data() {
        const termsStore = useTermsStore()
        const companyStore = useCompanyInfoStore()

        return {
            termDialog: false,
            deleteTermDialog: false,
            term: {
                company_info: null,
                term1: null,
                term2: null,
                term3: null,
                term4: null,
                term5: null
            },
            selectedTerm: null,
            submitted: false,
            dialogMode: 'create',
            loading: false,
            saveLoading: false,
            terms: [],
            companyInfo: null,
            termsStore,
            companyStore
        }
    },

    methods: {
        getEmptyTerm() {
            return {
                company_info: this.companyInfo.id,
                term1: null,
                term2: null,
                term3: null,
                term4: null,
                term5: null
            }
        },

        async openNew() {
            this.term = this.getEmptyTerm()
            this.submitted = false
            this.termDialog = true
            this.dialogMode = 'create'
        },

        hideDialog() {
            this.termDialog = false
            this.submitted = false
        },

        async editTerm(term) {
            try {
                this.term = { ...term }
                this.termDialog = true
                this.dialogMode = 'edit'
            } catch (error) {
                this.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Failed to load term data',
                    life: 3000
                })
            }
        },

        async saveTerm() {
            this.submitted = true

            try {
                if (this.dialogMode === 'create') {
                    await this.termsStore.createTerm(this.term)
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Success',
                        detail: 'Terms Created',
                        life: 3000
                    })
                } else {
                    await this.termsStore.updateTerm(this.term.id, this.term)
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Success',
                        detail: 'Terms Updated',
                        life: 3000
                    })
                }

                this.termDialog = false
                this.term = this.getEmptyTerm()
                await this.fetchTerms()
            } catch (error) {
                this.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: error.message || 'An error occurred',
                    life: 3000
                })
            }
        },

        confirmDelete(term) {
            this.term = term
            this.deleteTermDialog = true
        },

        async confirmDeleteTerm() {
            try {
                await this.termsStore.deleteTerm(this.term.id)
                this.deleteTermDialog = false
                this.term = this.getEmptyTerm()
                await this.fetchTerms()
                this.$toast.add({
                    severity: 'success',
                    summary: 'Success',
                    detail: 'Terms Deleted',
                    life: 3000
                })
            } catch (error) {
                this.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: error.message || 'An error occurred',
                    life: 3000
                })
            }
        },

        getAllTerms(term) {
            if (!term) return '';
            const terms = [term.term1, term.term2, term.term3, term.term4, term.term5]
                .filter(t => t) // Remove null/empty terms
                .join(' | ');
            return terms || 'No terms defined';
        },

        truncateText(text, length) {
            if (!text) return '';
            return text.length > length ? text.substring(0, length) + '...' : text;
        },

        onRowSelect(event) {
            this.selectedTerm = event.data
        },

        async fetchCompanies() {
            await this.fetchCompanyInfo();
            this.companies = this.companyInfo;
        },

        isTermField(key) {
            return /^term[1-5]$/.test(key);
        },

        async fetchTerms() {
            try {
                const terms = await this.termsStore.fetchTerms()
                this.terms = terms
                console.log('Fetched terms:', this.terms)
            } catch (error) {
                console.error('Error fetching terms:', error)
                this.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Failed to fetch terms',
                    life: 3000
                })
            }
        },

        async fetchCompanyInfo() {
            try {
                const response = await this.companyStore.fetchCompanyInfo()
                this.companyInfo = response || {}
            } catch (error) {
                console.error('Error fetching company info:', error)
                this.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: 'Failed to fetch company info',
                    life: 3000
                })
            }
        },

        getTermFields(term) {
            if (!term) return {};
            return Object.entries(term)
                .filter(([key]) => this.isTermField(key))
                .reduce((acc, [key, value]) => {
                    acc[key] = value;
                    return acc;
                }, {});
        }
    },

    async mounted() {
        try {
            await this.fetchCompanyInfo()
            await this.fetchTerms()
        } catch (error) {
            console.error('Initialization error:', error)
            this.$toast.add({
                severity: 'error',
                summary: 'Error',
                detail: 'Failed to initialize component',
                life: 3000
            })
        }
    }
}
</script>

<style scoped>
.header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #dee2e6;
}

.terms-container {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.term-item {
    background: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.term-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.term-header h3 {
    margin: 0;
    font-size: 1.1rem;
    color: #495057;
}

.term-content {
    margin: 0;
    color: #6c757d;
    white-space: pre-wrap;
}

/* Add this to your existing styles */
.button-group {
    display: flex;
    gap: 0.5rem;
    align-items: center;
}

/* Remove the term-actions class since we don't need it anymore */

.empty-state {
    text-align: center;
    padding: 3rem;
    color: #6c757d;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.card {
    padding: 2rem;
    border-radius: 8px;
    background: white;
    box-shadow: 0 2px 1px -1px rgba(0, 0, 0, 0.2),
        0 1px 1px 0 rgba(0, 0, 0, 0.14),
        0 1px 3px 0 rgba(0, 0, 0, 0.12);
}
</style>
