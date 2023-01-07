import React from "react";
import styles from "./Matches.module.scss";
import {get} from "../../functions/Requests/Requests";


const Matches = (props) => {
    const { tournament } = props;
    const [notFound, setNotFound] = React.useState(false);
    const [matches, setMatches] = React.useState([]);

    const getMatches = async () => {
        const matches_response = await get(`dashboard/tournament/${tournament}/matches`, { withCredentials: true }).catch(err => err.response);

        if (matches_response.status === 200) {
            if (matches_response.data.matches > 0) {
                setMatches(matches_response.data.matches);
            } else {
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
    } else { // TODO STYLE
        return (
            <div className="matches">
                {matches.map((match) => (
                        <div className="match">
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