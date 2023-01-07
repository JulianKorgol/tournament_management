import React from "react";
import User from "../../functions/UserContext/UserContext";
import { useNavigate } from "react-router";
import styles from "./PanelView.module.scss";
import { get } from "../../functions/Requests/Requests";


const PanelView = () => {
    const {user, checkLogin} = React.useContext(User);
    const [tournaments, setTournaments] = React.useState([]);
    const redirection = useNavigate();

    const checkUser = async () => {
        const logged = await checkLogin();
        if (!logged) {
            redirection("/login");
        }
        // console.log(user["role"]);
    }

    const tournamentsHandler = async () => {
        const response = await get("dashboard/", {withCredentials: true}).catch(err => err.response);
        if (response.status === 200) {
            setTournaments(response.data.tournaments);
        }
        console.log(tournaments);
    }

    React.useEffect(() => {
        checkUser();
        tournamentsHandler();
    }, []);

    return (
        <div className={styles.wrapper}>
            <h1>Panel</h1>
            <div className={styles.content}>
                <h2>Lista turniejów</h2>
                <p>O to lista turniejów, do których zostałaś/łeś przydzielona/ny. Wybierz za pomocą przycisku turniej,
                    którego szczegóły chcesz podejrzeć.</p>
            </div>
            <div className={styles.tournaments}>
                {tournaments.map((tournament) => (
                    <div key={tournament.uuid} className={styles.tournament}>
                        <h3>{tournament.name}</h3>
                        <p>Turniej toczy się w dniach:</p>
                        <p>{tournament.start_date}</p>
                        <p>{tournament.end_date}</p>
                        <p>Turniej publiczny: {tournament.public ? <i className="bi bi-check-lg"></i>
                            : <i className="bi bi-x"></i>}</p>
                        <a href={`/tournament/${tournament.uuid}`}>
                            <button className={styles.button}>Przejdź do turnieju</button>
                        </a>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default PanelView;