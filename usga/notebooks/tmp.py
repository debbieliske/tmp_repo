# Assume 'driver' is your connected Neo4j driver instance
# from the previous Python script.

# And assume the add_rule_node function is modified to accept a 'title'
# def add_rule_node(tx, rule_id, title, text, keywords=None, tags=None):
#     # ... (implementation would include SET r.title = $title)
#     pass

from neo4j import GraphDatabase, exceptions

# --- Database Connection --- (Assuming these are already defined as before)
# def get_neo4j_driver(uri, user, password): ...
# def close_neo4j_driver(driver): ...

# --- Modified Node Creation Function ---

def add_rule_node(tx, rule_id, title, text, keywords=None, tags=None):
    """
    Creates or updates a Rule node in the knowledge graph, including its title.

    This function uses a MERGE operation to ensure that a rule with a given
    rule_id is unique. If the node already exists, its properties (title, text,
    keywords, tags) are updated. Keywords and tags are stored as lists of strings.

    Args:
        tx (neo4j.Session.transaction): The Neo4j transaction object.
        rule_id (str): The unique identifier for the rule (e.g., "Rule 1", "Rule 1.1", "Rule 16.1a").
        title (str): The official title of the rule or sub-rule.
        text (str): The full text content of the rule or sub-rule.
        keywords (list, optional): A list of keywords associated with the rule. Defaults to an empty list.
        tags (list, optional): A list of tags (e.g., "Relief", "Penalty") for quick identification.
                              Defaults to an empty list.
    """
    if keywords is None:
        keywords = []
    if tags is None:
        tags = []

    # Cypher query to merge the Rule node.
    # MERGE attempts to match the pattern. If it exists, properties are updated (ON MATCH).
    # If it doesn't exist, the node is created and properties are set (ON CREATE).
    query = (
        "MERGE (r:Rule {rule_id: $rule_id}) "
        "ON CREATE SET "
        "  r.title = $title, "
        "  r.text = $text, "
        "  r.keywords = $keywords, "
        "  r.tags = $tags, "
        "  r.created_at = timestamp(), "
        "  r.updated_at = timestamp() "  # Set updated_at on creation as well for consistency
        "ON MATCH SET "
        "  r.title = $title, "
        "  r.text = $text, "
        "  r.keywords = $keywords, "
        "  r.tags = $tags, "
        "  r.updated_at = timestamp() "
        "RETURN r.rule_id AS id, r.title AS title" # Return some properties for confirmation
    )
    result = tx.run(query, rule_id=rule_id, title=title, text=text, keywords=keywords, tags=tags)
    record = result.single()
    if record:
        print(f"Rule node processed: ID='{record['id']}', Title='{record['title']}'")
    else:
        # This case should ideally not happen with MERGE unless there's an issue
        print(f"Warning: Rule node '{rule_id}' might not have been processed correctly.")


# --- Example Usage (Conceptual - you would call this from your PDF parsing script) ---
if __name__ == "__main__":
    # Replace with your Neo4j Aura credentials and URI
    NEO4J_URI = "neo4j+s://your_aura_db_id.databases.neo4j.io"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "your_aura_db_password"

    # --- Helper functions for connection (assuming they exist from prior code) ---
    def get_neo4j_driver(uri, user, password):
        try:
            driver = GraphDatabase.driver(uri, auth=(user, password))
            driver.verify_connectivity()
            print("Successfully connected to Neo4j.")
            return driver
        except Exception as e:
            print(f"Failed to create Neo4j driver: {e}")
            return None

    def close_neo4j_driver(driver):
        if driver:
            driver.close()
            print("Neo4j driver closed.")
    # --- End helper functions ---

    driver = get_neo4j_driver(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    if driver:
        try:
            # Example of how you would call this function with extracted data
            with driver.session(database="neo4j") as session:
                # --- Example for Rule 1 ---
                rule_1_id = "Rule 1"
                rule_1_title = "The Game, Player Conduct and the Rules"
                rule_1_text = "Purpose of Rule: Rule 1 introduces these central principles... (full text here)"
                session.execute_write(add_rule_node,
                                      rule_id=rule_1_id,
                                      title=rule_1_title,
                                      text=rule_1_text,
                                      keywords=["game principles", "player conduct", "spirit of the game"],
                                      tags=["Core Principle"])

                # --- Example for Rule 1.1 ---
                rule_1_1_id = "Rule 1.1"
                rule_1_1_title = "The Game of Golf"
                rule_1_1_text = "Golf is played in a round of 18 (or fewer) holes... (full text here)"
                session.execute_write(add_rule_node,
                                      rule_id=rule_1_1_id,
                                      title=rule_1_1_title,
                                      text=rule_1_1_text,
                                      keywords=["round", "course", "club", "stroke", "teeing area", "putting green"],
                                      tags=["Gameplay"])

                # --- Example for Rule 1.2a ---
                rule_1_2a_id = "Rule 1.2a"
                rule_1_2a_title = "Conduct Expected of All Players"
                rule_1_2a_text = "All players are expected to play in the spirit of the game by: Acting with integrity... (full text here)"
                session.execute_write(add_rule_node,
                                      rule_id=rule_1_2a_id,
                                      title=rule_1_2a_title,
                                      text=rule_1_2a_text,
                                      keywords=["integrity", "consideration", "safety", "care of course"],
                                      tags=["Player Conduct", "Etiquette"])

            print("\nSample rule nodes added to the knowledge graph.")

        except exceptions.Neo4jError as e:
            print(f"A Neo4j error occurred during database operations: {e} (Code: {e.code})")
        except Exception as e:
            print(f"An unexpected error occurred during database operations: {e}")
        finally:
            close_neo4j_driver(driver)
    else:
        print("Could not connect to Neo4j. Exiting.")



if driver:
    try:
        with driver.session(database="usga-neo4j") as session:
            # --- RULE 1 ---
            session.execute_write(add_rule_node,
                                  rule_id="Rule 1",
                                  title="The Game, Player Conduct and the Rules",
                                  text="Purpose of Rule: Rule 1 introduces these central principles of the game for the player: Play the course as you find it and play the ball as it lies. Play by the Rules and in the spirit of the game. You are responsible for applying your own penalties if you breach a Rule, so that you cannot gain any potential advantage over your opponent in match play or other players in stroke play. ... (rest of Rule 1 overview text from PDF page 22 up to 1.1)")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.1",
                                  title="The Game of Golf",
                                  text="Golf is played in a round of 18 (or fewer) holes on a course by striking a ball with a club. Each hole starts with a stroke from the teeing area and ends when the ball is holed on the putting green (or when the Rules otherwise say the hole is completed). For each stroke, the player: Plays the course as they find it, and Plays the ball as it lies. But there are exceptions where the Rules allow the player to alter conditions on the course and require or allow the player to play the ball from a different place than where it lies.")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1", child_rule_id="Rule 1.1")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.2",
                                  title="Standards of Player Conduct",
                                  text="(Text for 1.2 before 1.2a starts on PDF page 22)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1", child_rule_id="Rule 1.2")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.2a",
                                  title="Conduct Expected of All Players",
                                  text="All players are expected to play in the spirit of the game by: Acting with integrity – for example, by following the Rules, applying all penalties, and being honest in all aspects of play. Showing consideration to others – for example, by playing at a prompt pace, looking out for the safety of others, and not distracting the play of another player. If a player plays a ball in a direction where there might be a danger of hitting someone, they should immediately shout a warning, such as the traditional warning of “fore”. Taking good care of the course – for example, by replacing divots, smoothing bunkers, repairing ball-marks, and not causing unnecessary damage to the course. There is no penalty under the Rules for failing to act in this way, except that the Committee may disqualify a player for acting contrary to the spirit of the game if it finds that the player has committed serious misconduct. “Serious misconduct” is player behaviour that is so far removed from what is expected in golf that the most severe sanction of removing a player from the competition is justified. Penalties other than disqualification may be imposed for player misconduct only if those penalties are adopted as part of a Code of Conduct under Rule 1.2b.")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.2", child_rule_id="Rule 1.2a")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.2b",
                                  title="Code of Conduct",
                                  text="The Committee may set its own standards of player conduct in a Code of Conduct adopted as a Local Rule. The Code may include penalties for breach of its standards, such as a one-stroke penalty or the general penalty. The Committee may also disqualify a player for serious misconduct in failing to meet the Code’s standards. See Committee Procedures, Section 5I (explaining the standards of player conduct that may be adopted). (Text from PDF page 23)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.2", child_rule_id="Rule 1.2b")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.3",
                                  title="Playing by the Rules",
                                  text="(Text for 1.3 before 1.3a starts on PDF page 23)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1", child_rule_id="Rule 1.3")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.3a",
                                  title="Meaning of “Rules”; Terms of the Competition",
                                  text="The term “Rules” means: Rules 1-25 and the definitions in these Rules of Golf, and Any “Local Rules” the Committee adopts for the competition or the course. Players are also responsible for complying with all “Terms of the Competition” adopted by the Committee (such as entry requirements, the form and dates of play, the number of rounds and the number and order of holes in a round). See Committee Procedures, Section 5C (Local Rules) and Section 8 (Full set of authorized Model Local Rules); Section 5A (Terms of the Competition). (Text from PDF page 23)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.3", child_rule_id="Rule 1.3a")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.3b",
                                  title="Applying the Rules",
                                  text="(Text for 1.3b before 1.3b(1) starts on PDF page 24)") # Placeholder for introductory text if any
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.3", child_rule_id="Rule 1.3b")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.3b(1)",
                                  title="Player Responsibility for Applying the Rules.",
                                  text="Players are responsible for applying the Rules to themselves: Players are expected to recognize when they have breached a Rule and to be honest in applying their own penalties. If a player knows they have breached a Rule that involves a penalty and deliberately fails to apply the penalty, the player is disqualified. If two or more players agree to ignore any Rule or penalty they know applies and any of those players have started the round, they are disqualified (even if they have not yet acted on the agreement). When it is necessary to decide questions of fact, a player is responsible for considering not only their own knowledge of the facts but also all other information that is reasonably available. A player may ask for help with the Rules from a referee or the Committee, but if help is not available in a reasonable time the player must play on and raise the issue with a referee or the Committee when they become available (see Rule 20.1). (Text from PDF page 24)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.3b", child_rule_id="Rule 1.3b(1)")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.3b(2)",
                                  title="Accepting Player’s “Reasonable Judgment” in Determining a Location When Applying the Rules.",
                                  text="Many Rules require a player to determine a spot, point, line, edge, area or other location under the Rules, such as: Estimating where a ball last crossed the edge of a penalty area, Estimating or measuring when dropping or placing a ball in taking relief, Replacing a ball on its original spot (whether the spot is known or estimated), Determining the area of the course where the ball lies, including whether the ball lies on the course, or Determining whether the ball touches or is in or on an abnormal course condition. Such determinations about location need to be made promptly and with care but often cannot be precise. So long as the player does what can be reasonably expected under the circumstances to make an accurate determination, the player’s reasonable judgment will be accepted even if, after the stroke is made, the determination is shown to be wrong by video evidence or other information. If a player becomes aware of a wrong determination before the stroke is made, it must be corrected (see Rule 14.5). (Text from PDF page 24)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.3b", child_rule_id="Rule 1.3b(2)")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.3c",
                                  title="Penalties",
                                  text="(Text for 1.3c before 1.3c(1) starts on PDF page 25)") # Placeholder for introductory text if any
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.3", child_rule_id="Rule 1.3c")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 1.3c(1)",
                                  title="Actions Giving Rise to Penalties.",
                                  text="A penalty applies when a breach of a Rule results from a player’s own actions or the actions of their caddie (see Rule 10.3c). A penalty also applies when: Another person takes an action that would breach the Rules if taken by the player or caddie and that person does so at the player’s request or while acting with the player’s authority, or The player sees another person about to take an action concerning the player’s ball or equipment that they know would breach the Rules if taken by the player or caddie and does not take reasonable steps to object or stop it from happening. (Text from PDF page 25)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 1.3c", child_rule_id="Rule 1.3c(1)")

            # ... (Continue for 1.3c(2), 1.3c(3), 1.3c(4)) ...

            # --- RULE 2 ---
            session.execute_write(add_rule_node,
                                  rule_id="Rule 2",
                                  title="The Course",
                                  text="Purpose of Rule: Rule 2 introduces the basic things every player should know about the course: There are five defined areas of the course, and There are several types of defined objects and conditions that can interfere with play. It is important to know the area of the course where the ball lies and the status of any interfering objects and conditions, because they often affect the player’s options for playing the ball or taking relief. ... (rest of Rule 2 overview text from PDF page 27 up to 2.1)")
            # No parent for Rule 2

            session.execute_write(add_rule_node,
                                  rule_id="Rule 2.1",
                                  title="Course Boundaries and Out of Bounds",
                                  text="Golf is played on a course whose boundaries are set by the Committee. Areas not on the course are out of bounds. (Text from PDF page 27)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 2", child_rule_id="Rule 2.1")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 2.2",
                                  title="Defined Areas of the Course",
                                  text="There are five areas of the course. (Text from PDF page 27 before 2.2a)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 2", child_rule_id="Rule 2.2")

            session.execute_write(add_rule_node,
                                  rule_id="Rule 2.2a",
                                  title="The General Area",
                                  text="The general area covers the entire course except for the four specific areas of the course described in Rule 2.2b. It is called the “general area” because: It covers most of the course and is where a player’s ball will most often be played until the ball reaches the putting green. It includes every type of ground and growing or attached objects found in that area, such as fairway, rough and trees. (Text from PDF page 27)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 2.2", child_rule_id="Rule 2.2a")

            # ... (Continue for Rule 2.2b, 2.2c, 2.3, 2.4) ...

            # --- RULE 3 ---
            session.execute_write(add_rule_node,
                                  rule_id="Rule 3",
                                  title="The Competition",
                                  text="Purpose of Rule: Rule 3 covers the three central elements of all golf competitions: Playing either match play or stroke play, Playing either as an individual or with a partner as part of a side, and Scoring either by gross scores (no handicap strokes applied) or net scores (handicap strokes applied). ... (rest of Rule 3 overview text from PDF page 30 up to 3.1)")
            # No parent for Rule 3

            session.execute_write(add_rule_node,
                                  rule_id="Rule 3.1",
                                  title="Central Elements of Every Competition",
                                  text="(Text for 3.1 before 3.1a starts on PDF page 30)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 3", child_rule_id="Rule 3.1")
            
            # ... (Continue for all sub-rules of Rule 3, e.g., 3.1a, 3.1a(1), 3.1a(2), 3.1b, 3.1c, 3.2, 3.2a, etc.) ...


            # --- RULE 4 ---
            session.execute_write(add_rule_node,
                                  rule_id="Rule 4",
                                  title="The Player’s Equipment",
                                  text="Purpose of Rule: Rule 4 covers the equipment that players may use during a round. Based on the principle that golf is a challenging game in which success should depend on the player’s judgment, skills and abilities, the player: Must use conforming clubs and balls, Is limited to no more than 14 clubs, and Is restricted in the use of other equipment that gives artificial help to their play. For detailed requirements for clubs, balls and other equipment and the process for consultation and submission of equipment for conformity review, see the Equipment Rules. (Text from PDF page 40 before 4.1)")
            # No parent for Rule 4

            session.execute_write(add_rule_node,
                                  rule_id="Rule 4.1",
                                  title="Clubs",
                                  text="(Text for 4.1 before 4.1a starts on PDF page 40)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 4", child_rule_id="Rule 4.1")

            # ... (Continue for all sub-rules of Rule 4, e.g., 4.1a, 4.1a(1), 4.1a(2), 4.1a(3), 4.1b, etc.) ...


            # --- RULE 5 ---
            session.execute_write(add_rule_node,
                                  rule_id="Rule 5",
                                  title="Playing the Round",
                                  text="Purpose of Rule: Rule 5 covers how to play a round – such as where and when a player may practise on the course before or during a round, when a round starts and ends and what happens when play has to stop or resume. Players are expected to: Start each round on time, and Play continuously and at a prompt pace during each hole until the round is completed. When it is a player’s turn to play, it is recommended that they make the stroke in no more than 40 seconds, and usually more quickly than that. (Text from PDF page 52 before 5.1)")
            # No parent for Rule 5

            session.execute_write(add_rule_node,
                                  rule_id="Rule 5.1",
                                  title="Meaning of Round",
                                  text="A “round” is 18 or fewer holes played in the order set by the Committee. When a round ends in a tie and play will go on until there is a winner: Tied Match Extended One Hole at a Time. This is the continuation of the same round, not a new round. Play-off in Stroke Play. This is a new round. A player is playing their round from when it starts until it ends (see Rule 5.3), except while play is stopped under Rule 5.7a. When a Rule refers to actions taken “during a round”, that does not include while play is stopped under Rule 5.7a unless the Rule says otherwise. (Text from PDF page 52)")
            session.execute_write(add_rule_hierarchy_relationship, parent_rule_id="Rule 5", child_rule_id="Rule 5.1")

            # ... (Continue for all sub-rules of Rule 5, e.g., 5.2, 5.2a, 5.2b, 5.3, 5.3a, etc.) ...

            print("\\nSuccessfully (conceptually) added Rules 1-5 and their hierarchy to the knowledge graph.")

        except Exception as e:
            print(f"An error occurred during (conceptual) database operations: {e}")
        # finally:
            # close_neo4j_driver(driver) # You would close it after all operations
    else:
        print("Could not connect to Neo4j. Exiting.")