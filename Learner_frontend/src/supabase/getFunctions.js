import { supabase } from '@/supabase/init.js'

export async function getUser() {
    try {
        const { data: { user }, error } = await supabase.auth.getUser();
        
        if (error) {
            console.error('Error fetching user:', error.message);
            throw new Error('Failed to fetch user: ' + error.message);
        }

        return user
    } catch (err) {
        console.error('Unexpected error in getUser:', err);
        throw new Error('An unexpected error occurred: ' + err.message);
    }
}

export async function getUserExtra({id = null, user_id= null} = {}) {
    try {
        let queryField = "user_id"
        let queryValue = null

        if (id) {
            queryField = "id"
            queryValue = id
        } else if (user_id) {
            queryValue = user_id
        } else {
            const user = await getUser()
            queryValue = user.id
        }

        const { data: extra, error } = await supabase
            .from('user')
            .select('*')
            .eq(queryField, queryValue);

        if (error) {
            console.error('Error fetching extra:', error.message);
            throw new Error('Failed to fetch extra: ' + error.message);
        }
        return extra
        
    } catch (err) {
        console.error('Unexpected error in getUserExtra:', err);
        throw new Error('An unexpected error occurred: ' + err.message);
    }
}

export async function getUserLimitations({id = null, user_id = null, extra_id = null} = {}) {
    try {

        let queryField = "extra_id"
        let queryValue = null

        if (id) {
            queryField = "id"
            queryValue = id
        } else if (extra_id) {
            queryValue = extra_id
        } else if (user_id) {
            const extra = await getUserExtra({user_id : user_id})
            queryValue = extra[0].id
        } else {
            const extra = await getUserExtra()
            queryValue = extra[0].id
        }

        const { data: limit, error } = await supabase
            .from('limitations')
            .select('*')
            .eq(queryField, queryValue);

        if (error) {
            console.error('Error fetching limitations:', error.message);
            throw new Error('Failed to fetch limitations: ' + error.message);
        }

        return limit
    } catch (err) {
        console.error('Unexpected error in getUserLimitations:', err);
        throw new Error('An unexpected error occurred: ' + err.message);
    }
}

export async function getTeam({ id = null, creator_id = null, name = null, user_id = null, extra_id = null } = {}) {
    try {
        let queryField = null
        let queryValue = null
        let useIn = false

        if (id) {
            queryField = "id"
            queryValue = id
        } else if (creator_id) {
            queryField = "creator_id"
            queryValue = creator_id
        } else if (name) {
            queryField = "name"
            queryValue = name
        } else if (extra_id) {
            const extra = await getUserExtra({ id : extra_id })
            if (!extra.length || !extra[0]?.teams) {
                queryValue = [0]
            } else {
                queryValue = extra[0].teams
            }
            queryField = "id"
            useIn = true
        } else if (user_id) {
            const extra = await getUserExtra({ user_id : user_id })
            if (!extra.length || !extra[0]?.teams) {
                queryValue = [0]
            } else {
                queryValue = extra[0].teams
            }
            queryField = "id"
            useIn = true
        } else {
            const extra = await getUserExtra()
            if (!extra.length || !extra[0]?.teams) {
                queryValue = [0]
            } else {
                queryValue = extra[0].teams
            }
            queryField = "id"
            useIn = true
        }

        if (!queryField || !queryValue) {
            throw new Error(`Invalid query parameters provided`);
        }

        const { data: teams, error } = await supabase
            .from('team')
            .select('*')
            [useIn ? 'in' : 'eq'](queryField, queryValue);

        if (error) {
            console.error(`Error fetching team(s) by ${queryField}:`, error.message);
            throw new Error(`Failed to fetch team(s): ${error.message}`);
        }

        return teams
    } catch (err) {
        console.error('Unexpected error in getTeams:', err);
        throw new Error('An unexpected error occurred: ' + err.message);
    }
}

export async function getLesson({ id = null, creator_id = null, name = null, user_id = null, team_id = null } = {}) {
    try {
        let queryField = "creator_id"
        let queryValue = null

        if (id) {
            queryField = "id"
            queryValue = id
        } else if (creator_id) {
            queryValue = creator_id
        } else if (name) {
            queryField = "name"
            queryValue = name
        } else if (user_id) {
            const extra = await getUserExtra({user_id : user_id})
            queryValue = extra[0].id
        } else if (team_id) {
            queryField = "team_id"
            queryValue = team_id
        } else {
            const extra = await getUserExtra()
            queryValue = extra[0].id
        }

        const { data: lesson, error } = await supabase
            .from('lesson')
            .select('*')
            .eq(queryField, queryValue);

        if (error) {
            console.error('Error fetching lesson:', error.message);
            throw new Error('Failed to fetch lesson: ' + error.message);
        }

        return lesson
    } catch (err) {
        console.error('Unexpected error in getLesson:', err);
        throw new Error('An unexpected error occurred: ' + err.message);
    }
}

export async function getContainer({ id = null, extra_id = null, user_id = null, lesson_id = null} = {}) {
    try {
        const queryParams = [];

        if (id) {
            queryParams.push({ field: "id", value: id });
        } else if (extra_id && lesson_id) {
            queryParams.push({ field: "user_id", value: extra_id });
            queryParams.push({ field: "lesson_id", value: lesson_id });
        } else if (user_id && lesson_id) {
            const extra = await getUserExtra({ user_id : user_id });
            queryParams.push({ field: "user_id", value: extra[0]?.id });
            queryParams.push({ field: "lesson_id", value: lesson_id });
        } else if (lesson_id) {
            queryParams.push({ field: "lesson_id", value: lesson_id });
        } else {
            const extra = await getUserExtra();
            queryParams.push({ field: "user_id", value: extra[0]?.id });
            queryParams.push({ field: "lesson_id", value: lesson_id });
        }

        if (!queryParams.length) {
            return []
        }

        let query = supabase.from('container').select('*');
        for (const { field, value } of queryParams) {
            query = query.eq(field, value);
        }

        const { data: container, error } = await query;

        if (error) {
            console.error("Error fetching container:", error.message);
            throw new Error("Failed to fetch container: " + error.message);
        }

        return container;
    } catch (err) {
        console.error('Unexpected error in getContainer:', err);
        throw new Error('An unexpected error occurred: ' + err.message);
    }
}