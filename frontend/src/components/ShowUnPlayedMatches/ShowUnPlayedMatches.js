import React from "react";
import styles from './ShowUnPlayedMatches.module.scss'
import { get } from "../../functions/Requests/Requests";


const ShowUnPlayedMatches = (props) => {
    const [unPlayedMatches, setUnPlayedMatches] = React.useState([]);
    const { uuid } = props;

    const getUnPlayedMatches = async () => {
        const response = await get(`coordinator_panel/tournament/${uuid}/games/getnotplayed/`, {withCredentials: true}).catch(err => err.response);

        if (response.status === 200) {
            setUnPlayedMatches(response.data.games);
        }
    }

    React.useEffect(() => {
        getUnPlayedMatches();
    }, []);

    return (
        <div className={styles.wrapper}>
            <h4>Nierozegrane mecze</h4>
            <div className={styles.matches}>
                {unPlayedMatches.map((match, index) => (
                    <div className={styles.match} key={match.id}>
                        <p>{match.player1} - {match.player2}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ShowUnPlayedMatches;