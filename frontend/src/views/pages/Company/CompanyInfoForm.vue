<template>
    <div class="grid">
        <div class="col-12">
            <Card>
                <template #title>
                    <div class="flex justify-content-between align-items-center mb-3">
                        <h2 class="text-2xl font-bold m-0">Company Information</h2>
                    </div>
                </template>

                <template #content>
                    <form @submit.prevent="submitForm">
                        <div class="flex flex-col md:flex-row gap-8">
                            <!-- Left Column -->
                            <div class="md:w-1/2">
                                <!-- Basic Info Card -->
                                <div class="card flex flex-col gap-4 mb-4">
                                    <div class="font-semibold text-xl">Basic Information</div>
                                    <div class="flex flex-col gap-2">
                                        <label for="name">Company Name *</label>
                                        <InputText id="name" v-model="form.name" required />
                                    </div>
                                    <div class="flex flex-col gap-2">
                                        <label for="pincode">Pincode</label>
                                        <InputText id="pincode" v-model="form.pincode" maxlength="10" />
                                    </div>
                                </div>

                                <!-- Additional Details Card -->
                                <div class="card flex flex-col gap-4">
                                    <div class="font-semibold text-xl">Additional Details</div>
                                    <div class="flex flex-wrap gap-4">
                                        <div class="flex flex-col grow basis-0 gap-2">
                                            <label for="sub_head1">Sub Head 1</label>
                                            <InputText id="sub_head1" v-model="form.sub_head1" />
                                        </div>
                                        <div class="flex flex-col grow basis-0 gap-2">
                                            <label for="sub_head2">Sub Head 2</label>
                                            <InputText id="sub_head2" v-model="form.sub_head2" />
                                        </div>
                                        <div class="flex flex-col grow basis-0 gap-2">
                                            <label for="sub_head3">Sub Head 3</label>
                                            <InputText id="sub_head3" v-model="form.sub_head3" />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- Right Column -->
                            <div class="md:w-1/2">
                                <!-- Contact Info Card -->
                                <div class="card flex flex-col gap-4 mb-4">
                                    <div class="font-semibold text-xl">Contact Information</div>
                                    <div class="grid grid-cols-12 gap-2">
                                        <label for="c_phone"
                                            class="flex items-center col-span-12 mb-2 md:col-span-3">Phone</label>
                                        <div class="col-span-12 md:col-span-9">
                                            <InputText id="c_phone" v-model="form.c_phone" maxlength="20"
                                                class="w-full" />
                                        </div>
                                    </div>
                                    <div class="grid grid-cols-12 gap-2">
                                        <label for="c_mobile"
                                            class="flex items-center col-span-12 mb-2 md:col-span-3">Mobile</label>
                                        <div class="col-span-12 md:col-span-9">
                                            <InputText id="c_mobile" v-model="form.c_mobile" maxlength="20"
                                                class="w-full" />
                                        </div>
                                    </div>
                                    <div class="grid grid-cols-12 gap-2">
                                        <label for="c_mail"
                                            class="flex items-center col-span-12 mb-2 md:col-span-3">Email</label>
                                        <div class="col-span-12 md:col-span-9">
                                            <InputText id="c_mail" v-model="form.c_mail" type="email" class="w-full" />
                                        </div>
                                    </div>
                                </div>

                                <!-- Tax Info Card -->
                                <div class="card flex flex-col gap-4">
                                    <div class="font-semibold text-xl">Tax Information</div>
                                    <div class="flex flex-wrap gap-4">
                                        <div class="flex flex-col grow basis-0 gap-2">
                                            <label for="gstin">GSTIN</label>
                                            <InputText id="gstin" v-model="form.gstin" maxlength="15" />
                                        </div>
                                        <div class="flex flex-col grow basis-0 gap-2">
                                            <label for="pan">PAN</label>
                                            <InputText id="pan" v-model="form.pan" maxlength="20" />
                                        </div>
                                    </div>
                                    <div class="flex flex-wrap gap-4">
                                        <div class="flex flex-col grow basis-0 gap-2">
                                            <label for="cst">CST</label>
                                            <InputText id="cst" v-model="form.cst" maxlength="20" />
                                        </div>
                                        <div class="flex flex-col grow basis-0 gap-2">
                                            <label for="tin_no">TIN</label>
                                            <InputText id="tin_no" v-model="form.tin_no" maxlength="20" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Banking Details - Full Width -->
                        <div class="card flex flex-col gap-4 mt-8">
                            <div class="font-semibold text-xl">Banking Information</div>
                            <div class="flex flex-wrap">
                                <label for="bank">Bank Details</label>
                                <Textarea id="bank" v-model="form.bank" rows="4" class="w-full" />
                            </div>
                        </div>

                        <!-- Action Buttons -->
                        <div class="flex justify-content-end gap-2 mt-4">
                            <Button type="button" label="Delete" severity="danger" @click="deleteCompanyInfo" />
                            <Button type="submit" label="Save" severity="success" />
                        </div>
                    </form>
                </template>
            </Card>
        </div>
    </div>
    <ConfirmDialog></ConfirmDialog>
</template>

<script>
import { useCompanyInfoStore } from '../../../store/companyInfo';
import { useToast } from 'primevue/usetoast';

export default {
    data() {
        return {
            companyInfoStore: useCompanyInfoStore(),
            toast: useToast(),
            form: {
                name: '',
                sub_head1: '',
                sub_head2: '',
                sub_head3: '',
                c_phone: '',
                c_fax: '',
                c_mail: '',
                c_mobile: '',
                cst: '',
                tin_no: '',
                gstin: '',
                pan: '',
                bank: '',
                pincode: ''
            },
            loading: false,
        };
    },
    methods: {
        navigateBack() {
            this.$router.push({ name: 'dashboard' });
        },
        async submitForm() {
            this.loading = true;
            try {
                const companyStore = useCompanyInfoStore();
                if (this.form.id) {
                    const result = await companyStore.updateCompanyInfo(this.form);
                    if (result.success) {
                        this.$toast.add({
                            severity: 'success',
                            summary: 'Success',
                            detail: 'Company information Updated successfully',
                            life: 3000
                        });
                        this.navigateBack();
                    } else {
                        this.showToastError(result.data.data);
                    }
                } else {
                    const result = await companyStore.saveCompanyInfo(this.form);
                    if (result.success) {
                        this.$toast.add({
                            severity: 'success',
                            summary: 'Success',
                            detail: 'Company information saved successfully',
                            life: 3000
                        });
                        this.navigateBack();
                    } else {
                        console.log(result.data.data.errors);
                        this.showToastError(result.data.data);
                    }
                }
            } finally {
                this.loading = false;
            }
        },
        async deleteCompanyInfo() {
            this.$confirm.require({
                message: 'Are you sure you want to delete this company information?',
                header: 'Confirm Delete',
                icon: 'pi pi-exclamation-triangle',
                accept: async () => {
                    const companyStore = useCompanyInfoStore();
                    await companyStore.deleteCompanyInfo();
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Success',
                        detail: 'Company information deleted successfully',
                        life: 3000
                    });
                    this.navigateBack();
                }
            });
        },
        showToastError(errorResponse) {
            console.log("errorResponse:", errorResponse);

            if (errorResponse.message) {
                this.$toast.add({
                    severity: 'error',
                    summary: 'Error',
                    detail: errorResponse.message,
                    life: 3000,
                });
            }
            if (errorResponse.errors) {
                for (const [field, messages] of Object.entries(errorResponse.errors)) {
                    messages.forEach((message) => {
                        this.$toast.add({
                            severity: 'error',
                            summary: `Error in ${field}`,
                            detail: message,
                            life: 3000,
                        });
                    });
                }
            }
        }
    },
    async mounted() {
        const companyStore = useCompanyInfoStore();
        await companyStore.fetchCompanyInfo();
        this.form = this.companyInfoStore.companyInfo;
    }
};
</script>

<style scoped>
.card {
    background: var(--surface-card);
    padding: 1.5rem;
    border-radius: 6px;
    box-shadow: 0 2px 1px -1px rgba(0, 0, 0, .2), 0 1px 1px 0 rgba(0, 0, 0, .14), 0 1px 3px 0 rgba(0, 0, 0, .12);
}

.field {
    margin-bottom: 1.5rem;
}

label {
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.grow {
    flex-grow: 1;
}

.basis-0 {
    flex-basis: 0;
}
</style>
