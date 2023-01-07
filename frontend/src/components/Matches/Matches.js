import React from "react";
import styles from "./Matches.module.scss";
import {get} from "../../functions/Requests/Requests";


const Matches = (props) => {
    const { tournament } = props;
    const [notFound, setNotFound] = React.useState(false);
    const [matches, setMatches] = React.useState([]);

    const getMatches = async () => {
        const matches_response = await get(`dashboard/tournament/${tournament}/matches`, { withCredentials: true }).catch(err => err.response);
        console.log(matches_response);

        if (matches_response.status === 200) {
            setMatches(matches_response.data.games);
            if (matches_response.data.error === "No games to show") {
                setNotFound(true);
            }
        }
    }

    React.useEffect(() => {
        getMatches();
    }, []);

    if (notFound) {
        return (
            <div className={styles.error}>
                <h5>Brak meczy</h5>
            </div>
        )
    } else {
        return (
            <div className={styles.matches}>
                {matches.map((match) => (
                        <div key={match.player1 + match.player2} className={styles.match}>
                            <p>{match.player1} - {match.player2}</p>
                            <p>{match.player1_score}:{match.player2_score}</p>
                            <p>{match.date}</p>
                        </div>
                ))}
            </div>
        )
    }
}

export default Matches;