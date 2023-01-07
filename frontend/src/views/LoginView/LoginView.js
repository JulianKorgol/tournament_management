import React from "react";
import axios from "axios"
import styles from "./LoginView.module.scss";
import Cookies from "js-cookie"
import { get, post } from "../../functions/Requests/Requests";
import AppContext from "../../functions/AppContext/AppContext";
import { useNavigate } from "react-router";
import User from "../../functions/UserContext/UserContext";



const Login = () => {
    const { setLoading, MakeToast } = React.useContext(AppContext);
    const { checkLogin } = React.useContext(User);
    const redirection = useNavigate();

    const loginuser = async (username, password) => {
        axios.defaults.withCredentials = true;
        const response = await post("login/", {username: username, password: password}, { withCredentials: true }).catch(err => err.response);
        Cookies.set("csrftoken", response.data.csrftoken);
        Cookies.set("sessionid", response.data.sessionid);

        if (response.status === 200) {
            const userInfo = await get("me/", { withCredentials: true }).catch(err => err.response);
            Cookies.set("role", userInfo.data.role);

            if (userInfo.status === 200) {
                axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
                return true;
            }
        }
        return false;
    }

    const formSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const username = e.target.username.value;
        const password = e.target.password.value;

        const login_entry = await loginuser(username, password);

        if (login_entry) {
            setLoading(false);
            MakeToast("Logowanie powiodło się", "success");
            setTimeout(() => {
                redirection("/panel");
            }, 1000);
            return
        }

        setLoading(false);
        MakeToast("Logowanie nie powiodło się", "error");
    }

    const checkAlreadyLogged = async () => {
        const logged = await checkLogin();
        if (logged) {
            redirection("/panel");
        }
    }

    React.useEffect(() => {
        checkAlreadyLogged();
    }, []);


    return (
        <div className={styles.wrapper}>
            <h4 className={styles.subtitle}>Witaj ponownie :)</h4>
            <h1 className={styles.title}>Logowanie!</h1>
            <div className={styles.form}>
                <form onSubmit={formSubmit}>
                    <div className={styles.formContent}>
                        <label className={styles.label} htmlFor="username">Nazwa użytkownika</label>
                        <input className={styles.input} type="text" name="username" id="username" />
                    </div>
                    <div className={styles.formContent}>
                        <label className={styles.label} htmlFor="password">Hasło</label>
                        <input className={styles.input} type="password" name="password" id="password" />
                    </div>
                    <div className={styles.formButton}>
                        <button className={styles.button} type="submit">Zaloguj</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login;
