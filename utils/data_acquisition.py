import pandas as pd
from cartolafc import Api
from cartolafc.constants import MERCADO_FECHADO


def get_players() -> pd.DataFrame:
    """Get players available in the market"""
    api = Api()
    players = api.mercado_atletas()
    records = []
    for player in players:
        player_record = {
            "nickname": player.apelido,
            "id": player.id,
            "position": player.posicao.abreviacao,
            "price": player.preco,
            "team": player.clube.abreviacao,
            "status": player.status.nome
        }
        records.append(player_record)
    return pd.DataFrame.from_records(records)


def get_matches() -> pd.DataFrame:
    """Get all matches until the current round (not_included)"""

    api = Api()
    max_rounds = api.mercado().rodada_atual 

    records = []
    for round in range(1, max_rounds):
        matches = api.partidas(round)
        for match in matches:
            match_record = {
                "date": match.data,
                "home_team": match.clube_casa.abreviacao,
                "away_team": match.clube_visitante.abreviacao,
                "home_score": match.placar_casa,
                "away_score": match.placar_visitante,
                "round": round
            }
            records.append(match_record)
    
    return pd.DataFrame.from_records(records)


def get_next_match() -> pd.DataFrame:
    """Get the next match in the championship"""
    api = Api()
    market = api.mercado() 
    next_round = market.rodada_atual

    if market.status.id == MERCADO_FECHADO:
        next_round += 1
    
    records = []
    matches = api.partidas(next_round)
    for match in matches:
        match_record = {
            "date": match.data,
            "home_team": match.clube_casa.abreviacao,
            "away_team": match.clube_visitante.abreviacao,
            "round": next_round
        }
        records.append(match_record)
    # TODO: Add team position in this output

    return pd.DataFrame.from_records(records)



def get_players_perfomance() -> pd.DataFrame:
    """Get players perfomance information along the rounds"""

    api = Api()
    max_rounds = api.mercado().rodada_atual 

    records = []
    for round in range(1, max_rounds):
        players_round = list(api.resultados_atletas(round).values())
        for player in players_round:
            if player.entrou_em_campo:
                record = {
                    "nickname": player.apelido,
                    "id": player.id,
                    "position": player.posicao.abreviacao,
                    "price": player.preco,
                    "team": player.clube.abreviacao,
                    "points": player.pontos,
                    "round": round
                }
                records.append(record)
    
    return pd.DataFrame.from_records(records)
    

