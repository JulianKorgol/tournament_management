import React from "react";
import axios from "axios"
import styles from "./LoginView.module.scss";
import Cookies from "js-cookie"
import { post } from "../../functions/Requests/Requests";
import AppContext from "../../functions/AppContext/AppContext";
import { useToast } from "@chakra-ui/react";


const Login = (email, password) => {
    const { loadingHandler } = React.useContext(AppContext);
    const toast = useToast({ isClosable: true, position: "bottom-right", duration: 5000 });


    const loginuser = async () => {
        const response = await post("login/", {email: email, password: password});

        if (response.status === 200) {
            axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken")
            return True;
        }
        return False;
    }

    const formSubmit = (e) => {
        e.preventDefault();
        loadingHandler();
        const email = e.target.email.value;
        const password = e.target.password.value;
        const login_entry = loginuser(email, password);
        console.log(login_entry)
        if (login_entry) {
            loadingHandler();
            toast({title: "Zalogowano pomyślnie", status: "success"});
        }
        loadingHandler();
        toast({title: "Błąd logowania. Spróbuj ponownie.", status: "error"});
    }


    return (
        <div className={styles.wrapper}>
            <h4 className={styles.subtitle}>Witaj ponownie :)</h4>
            <h1 className={styles.title}>Logowanie!</h1>
            <div className={styles.form}>
                <form onSubmit={formSubmit}>
                    <div className={styles.formContent}>
                        <label className={styles.label} htmlFor="email">Email</label>
                        <input className={styles.input} type="email" name="email" id="email" />
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
