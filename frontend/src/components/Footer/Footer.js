import React from "react";
import styles from "./Footer.module.scss";


const Footer = () => {
    return (
        <div className={styles.footer}>
            <hr />
            <div className={styles.footerContent}>
                <a href="https://juliankorgol.com/" target="_blank">Made by: Julian Korgol</a>
                <p>in React and Django ❤️</p>
            </div>
        </div>
    );
}

export default Footer;
