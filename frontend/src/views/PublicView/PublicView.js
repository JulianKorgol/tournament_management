import React from "react";
import { useNavigate } from "react-router";
import styles from "./PublicView.module.scss";
import { get } from "../../functions/Requests/Requests";


const PublicView = () => {
    const [tournaments, setTournaments] = React.useState([]);
    const redirection = useNavigate();

    const tournamentsHandler = async () => {
        const response  = await get("public/tournaments/").catch(err => err.response);
        if (response.status === 200) {
            setTournaments(response.data.tournaments);
        }
    }

    React.useEffect(() => {
        tournamentsHandler();
    }, []);

    return (
        <div className={styles.wrapper}>
            <div className={styles.content}>
                <h2>Lista turniejów</h2>
                <p>O to lista publicznych turniejów.</p>
            </div>
            <div className={styles.tournaments}>
                {tournaments.map((tournament) => (
                    <div key={tournament.uuid} className={styles.tournament}>
                        <h3>{tournament.name}</h3>
                        <p>Turniej toczy się w dniach:</p>
                        <p>{tournament.start_date}</p>
                        <p>{tournament.end_date}</p>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default PublicView;