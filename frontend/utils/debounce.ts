export const debounce = <T extends (...args: any[]) => void>(
    func: T,
    timeout: number,
): ((...args: Parameters<T>) => void) => {
    let timeoutId: NodeJS.Timeout | null = null;

    return (...args: Parameters<T>): void => {
        if (timeoutId) {
            clearTimeout(timeoutId);
        }
        timeoutId = setTimeout(() => {
            func(...args);
        }, timeout);
    };
};
