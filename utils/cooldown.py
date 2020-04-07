import time


class CooldownHandler:
    # Data in the form:
    # userId: {cooldownId: time, ...}
    # where _time_ is the epoch time at which the cooldown expires
    cooldown_data = {}

    @staticmethod
    def setCooldown(userId, cooldownId, running_time):
        """

        :param userId: discord id
        :param cooldownId:
        :param running_time: in seconds
        :return:
        """
        user_cooldowns = CooldownHandler.getCooldowns(userId)

        if user_cooldowns is None:
            user_cooldowns = {}

        user_cooldowns[cooldownId] = time.time() + running_time

        CooldownHandler.cooldown_data[userId] = user_cooldowns

    @staticmethod
    def getCooldowns(userId):
        """

        :param userId: discord id
        :return: a dictionary of cooldowns for that user, null if they don't have any
        """
        if userId not in CooldownHandler.cooldown_data:
            return None

        return CooldownHandler.cooldown_data.get(userId)

    @staticmethod
    def getCooldownTime(userId, cooldownId):
        """

        :param userId: discord id
        :param cooldownId:
        :return: return time in second until the cooldown finishes, -1 if there is no cooldown for this
        """
        user_cooldown = CooldownHandler.getCooldowns(userId)

        if user_cooldown is None:
            return -1

        if cooldownId not in user_cooldown.keys():
            return -1

        return user_cooldown[cooldownId] - time.time()

    @staticmethod
    def isOnCooldown(userId, cooldownId):
        """

        :param userId:
        :param cooldownId:
        :return: true if active for that cooldown
        """
        return CooldownHandler.getCooldownTime(userId, cooldownId) > 0
