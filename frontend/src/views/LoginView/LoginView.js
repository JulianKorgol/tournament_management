import React from "react";
import axios from "axios"
import styles from "./LoginView.module.scss";
import Cookies from "js-cookie"
import { get, post } from "../../functions/Requests/Requests";
import AppContext from "../../functions/AppContext/AppContext";
import Toast from "../../functions/Toast/Toast";



const Login = () => {
    const { setLoading } = React.useContext(AppContext);
    const [open, setOpen] = React.useState(false);
    const [message, setMessage] = React.useState("");
    const [status, setStatus] = React.useState("success");


    const MakeToast = (message, status) => {
        setMessage(message);
        setStatus(status);
        setOpen(true);
        setTimeout(() => {
            setOpen(false);
        }, 6000);
    }


    const loginuser = async (username, password) => {
        const response = await post("login/", {username: username, password: password}).catch(err => err.response);

        if (response.status === 200) {
            console.log(response);
            const userInfo = await get("me/", { withCredentials: true }).catch(err => err.response);
            console.log(userInfo);
            if (userInfo.status === 200) {
                axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
                return true;
            }
        }
        return false;
    }

    const formSubmit = async (e) => {
        e.preventDefault();
        setOpen(false);
        setLoading(true);

        const username = e.target.username.value;
        const password = e.target.password.value;

        const login_entry = await loginuser(username, password);

        if (login_entry) {
            setLoading(false);
            MakeToast("Logowanie powiodło się", "success");
            return
        }

        MakeToast("Logowanie nie powiodło się", "error");
        setLoading(false);
    }


    return (
        <div className={styles.wrapper}>
            <h4 className={styles.subtitle}>Witaj ponownie :)</h4>
            <h1 className={styles.title}>Logowanie!</h1>
            <div className={styles.form}>
                <form onSubmit={formSubmit}>
                    <div className={styles.formContent}>
                        <label className={styles.label} htmlFor="username">Email</label>
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
            {open ? <Toast message={message} status={status} /> : null}
        </div>
    );
}

export default Login;
