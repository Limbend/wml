import { useMessage, type IMessagePayload } from '~/store/toastMessages';

export const messageHandler = (message: IMessagePayload) => {
    const { SET_MESSAGE } = useMessage();
    SET_MESSAGE(message);
};
