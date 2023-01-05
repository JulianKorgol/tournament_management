import React from "react";
import styles from "./NotFoundView.module.scss";


const NotFound = () => {
    return (
        <div className={styles.wrapper}>
            <h1>404</h1>
            <h2>Page not found</h2>
        </div>
    );
}

export default NotFound;
