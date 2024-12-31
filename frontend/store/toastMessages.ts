import { defineStore } from 'pinia';
import { useToast } from 'primevue/usetoast';

export interface IMessagePayload {
    type: 'success' | 'info' | 'warn' | 'error' | undefined;
    message: string | undefined;
}

export const useMessage = defineStore('message', () => {
    const toast = useToast();

    const SET_MESSAGE = (payload: IMessagePayload) => {
        toast.add({
            severity: payload?.type,
            summary: 'Уведомление',
            detail: payload?.message,
            life: 3000,
            group: 'message',
        });
    };

    return { SET_MESSAGE };
});
