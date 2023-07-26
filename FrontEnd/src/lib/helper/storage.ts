export enum UserStorage {
	UserToken = 'USER_TOKEN'
}

export const getUserToken = () => localStorage.getItem(UserStorage.UserToken);

export const setUserToken = (token: string) => localStorage.setItem(UserStorage.UserToken, token);
