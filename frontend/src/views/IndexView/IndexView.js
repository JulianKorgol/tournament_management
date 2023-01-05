import React from "react";
import styles from "./IndexView.module.scss";


const IndexView = () => {
    return (
        <div className={styles.wrapper}>
            <div className={styles.welcome}>
                <h4 className={styles.subtitle}>Proste zarządzanie turniejami</h4>
                <h1 className={styles.title}>Aplikacja do zarządzania turniejami</h1>
            </div>
            <div className={styles.section}>
                <img src="https://unsplash.it/700/600" alt="logo" />
            </div>
        </div>
    );
}

export default IndexView;
