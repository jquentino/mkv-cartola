import pandas as pd
from cartolafc import Api

def get_players() -> pd.DataFrame:
    """Get players available in the market"""
    api = Api()
    players = api.mercado_atletas()
    records = []
    for player in players:
        player_record = {
            "nickname": player.apelido,
            "id": player.id,
            "position": player.posicao.abreviacao
        }
        records.append(player_record)
    return pd.DataFrame.from_records(records)
    

