from flask import jsonify, request, current_app
from polzybackend.gamification import bp
from polzybackend.models import GamificationBadge, GamificationBadgeType
from polzybackend import auth


@bp.route('/badges')
@auth.login_required
def badges():
    #
    # returns list of all user badges
    #

    try:
        badges = [badge.to_json() for badge in auth.current_user().badges]
        return jsonify(badges), 200
    except Exception as e:
        current_app.logger.exception(f'Faild to get Gamification Badges: {e}')
        return jsonify({'error': 'Bad Request'}), 400


@bp.route('/badges/seen', methods=['POST'])
@auth.login_required
def make_badge_seen():
    #
    # makes the bage as seen
    #

    try:

        # get request data and badge
        data = request.get_json()
        badge = data.get('badge')
        if badge is None:
            raise Exception('Badge data not found in request')

        # find badge in user badges
        userBadge = list(filter(lambda x: x.type.name == badge.get('type'), auth.current_user().badges))
        if len(userBadge) == 0:
            raise Exception(f"Badge Type {badge.type} not found in user's badges")

        # update badge instance
        userBadge[0].set_seen()

        # return updated lit of badges
        return jsonify([badge.to_json() for badge in auth.current_user().badges]), 200

    except Exception as e:
        current_app.logger.exception(f'Making Gamification Badge seen fails: Badge={badge}\n{e}')
        return jsonify({'error': 'Bad Request'}), 400


@bp.route('/badges/types')
@auth.login_required
def badge_types():
    #
    # returns list of available types of badges
    #

    try:
        badge_types = GamificationBadgeType.query.order_by('id').all()
        return jsonify([badge.to_json() for badge in badge_types]), 200
    except Exception as e:
        current_app.logger.exception(f'Faild to get Gamification Badge Types: {e}')
        return jsonify({'error': 'Bad Request'}), 400


@bp.route('/rankings')
@auth.login_required
def rankings():
    #
    # returns user's rankings
    #

    # waiting delay
    from time import sleep
    sleep(3)

    rank_categories = [
        'weekly',
        'monthly',
        'annual',
    ]

    rank_topics = [
        "KFZ FastOffer",
        "Wohnen Fastofffer",
        "Policy Cancellations",
    ]

    # generate random ranking
    from random import randrange
    ranking_data = {category: [
        {
            'name': f'{category.capitalize()} {topic}',
            'operations': randrange(10000),
            'rank': randrange(100),
        } for topic in rank_topics 
    ] for category in rank_categories}

    return jsonify(ranking_data), 200
