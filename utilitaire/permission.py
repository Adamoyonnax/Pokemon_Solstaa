# ID des rôles qui pourront utiliser les commande_admins en dehors des administrateurs
ROLE_ADMIN_ID = 123456789012345678


def est_admin(interaction):
    # Administrateur Discord
    if interaction.user.guild_permissions.administrator:
        return True

    # Rôle spécifique
    return any(
        role.id == ROLE_ADMIN_ID
        for role in interaction.user.roles
    )