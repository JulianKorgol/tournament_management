import React from "react";
import User from "../../functions/UserContext/UserContext";
import { useNavigate } from "react-router";
import styles from "./PanelView.module.scss";
import { get } from "../../functions/Requests/Requests";


const PanelView = () => {
    const {user, checkLogin} = React.useContext(User);
    const [tournaments, setTournaments] = React.useState([]);
    const [matches, setMatches] = React.useState([]);
    const [privileged, setPrivileged] = React.useState(false);
    const redirection = useNavigate();
    let myRole;

    const checkUser = async () => {
        const logged = await checkLogin();
        if (!logged) {
            redirection("/login");
        }
    }

    const tournamentsHandler = async () => {
        const me_data = await get("me/", {withCredentials: true}).catch(err => err.response);
        const myRole = me_data.data.account.role;

        if (myRole === "admin" || myRole === "coordinator")
        {
            const response = await get("dashboard/", {withCredentials: true}).catch(err => err.response);
            if (response.status === 200) {
                setTournaments(response.data.tournaments);
            }
            setPrivileged(true);
        } else {
            const response = await get("me/games/", {withCredentials: true}).catch(err => err.response);
            if (response.status === 200) {
                setMatches(response.data.games);
            }
        }
    }

    React.useEffect(() => {
        checkUser();
        tournamentsHandler();
    }, []);

    return (
        <div className={styles.wrapper}>
            <h1>Panel</h1>
            { privileged ?
                <div>
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
            :
                <div>
                    <div className={styles.content}>
                        <h2>Lista Twoich meczy</h2>
                        <p>Oto lista meczy, do których zostałaś/łeś przydzielona/ny oraz ich wyniki.</p>
                    </div>
                    <div className={styles.matches}>
                        {matches.map((match) => (
                            <div className={styles.game} key={match.id}>
                                <p>Zawodnik: {match.player1} vs Zawodnik: {match.player2} {match.player1_score !== null && match.player2_score !== null ? (<p>{match.player1_score}:{match.player2_score}</p>) : <p>(nierozegrany)</p>}</p>
                            </div>
                        ))}
                    </div>
                </div>
            }
        </div>
    )
}

export default PanelView;