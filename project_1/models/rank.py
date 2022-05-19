class Rank:
    def __init__(
            self,
            rank_id=0,
            rank_name=''
    ):
        self.rank_id = rank_id
        self.rank_name = rank_name

    def json(self):
        return {
            'rankId': self.rank_id,
            'rankName': self.rank_name
        }

    def __repr__(self):
        return str(self.json())
    
