from common_util import PostGameStatsUtil

class PostGameStatDao:
    def get_player_id(self):
        player_id = PostGameStatsUtil.PostGameStatsUtil.get_player_id(self)
        return jsonify(int(player_id))