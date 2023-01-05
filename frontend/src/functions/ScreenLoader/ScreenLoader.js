import styles from "./ScreenLoader.module.scss";


const ScreenLoader = () => {
    return (
        <div className={styles.container}>
            <div className={styles.spinner}></div>
        </div>
    );
}

export default ScreenLoader;