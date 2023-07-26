export function requireAuth() {
	return (to, from, next) => {
		const token = localStorage.getItem("accessToken");

		// If token is not present, redirect the user to the login page
		if (!token) {
			return next("/login");
		}

		// Otherwise, allow access to the requested route
		return next();
	};
}
