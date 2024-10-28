import { useEffect, useState } from "react";
import axios from 'axios';

import Game from "./Game";

type Player =  {
    pid: number;
    name: string;
    score: number;
    ip: string;
};

export default function GamePage({ params } : { params: { code: string } }) {
    const [players, setPlayers] = useState<Player[]>([]);
    useEffect(() => {
        axios.get(`/api/sessions/${params.code}`).then((response) => {
            setPlayers(response.data);
        });
    })
    return (
        <Game />
    );
  }
  