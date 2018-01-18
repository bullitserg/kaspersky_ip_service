# login_ip_module
max_id_query = '''SELECT a.id -- максимальный текущий id
                            FROM httpActions a
                            WHERE a.code = 302
                            AND a.eventTypeId = 1
                            ORDER BY id DESC
                            LIMIT 1
                            ;'''

get_ip_query = '''SELECT DISTINCT a.remoteAddr
                                  FROM httpActions a
                                  WHERE a.code = 302
                                  AND a.eventTypeId = 1
                                  AND %(last_max_id)s <= a.id
                                  AND a.id < %(actual_max_id)s
                                  ORDER BY a.id DESC
                                  ;'''

get_bot_ip_query = '''SELECT
                      a.remoteAddr, COUNT(a.id) AS cnt
                    FROM httpActions a
                    WHERE a.dateTime > (SELECT
                                          SUBDATE(a1.dateTime, INTERVAL %(bot_check_time)s MINUTE) -- время проверки
                                          FROM httpActions a1
                                          WHERE a1.id = %(actual_max_id)s)
                    AND a.code = 302
                    AND a.eventTypeId = 1
                    AND a.id < %(actual_max_id)s -- актуальный id
                      GROUP BY a.remoteAddr
                      HAVING cnt > %(bot_authorization_limit)s -- предел авторизаций
                      ORDER BY cnt DESC
                    ;'''

add_ip_query = '''INSERT INTO kaspersky_actual_ip (ipAddress, addDateTime, ipType) VALUES (%s, NOW(), %s);'''

# send_ip_module
get_ip_for_send_query = '''SELECT kai.id, kai.ipAddress
FROM kaspersky_actual_ip kai
WHERE kai.isSend = 0
AND kai.active = 1;'''

sended_ip_setting_query = '''UPDATE kaspersky_actual_ip kai SET kai.isSend = 1
WHERE kai.id IN (%s);'''

# delete_ip_module
get_kaspersky_delete_login_ip_query = '''SELECT
    DISTINCT kai.ipAddress
  FROM kaspersky_actual_ip kai
  WHERE
  kai.ipAddress NOT IN (
SELECT
  DISTINCT kai1.ipAddress
FROM kaspersky_actual_ip kai1
WHERE kai1.active = 1
AND kai1.addDateTime >= SUBDATE(NOW(), INTERVAL %(delete_login_time)s MINUTE)
AND kai1.id >= (SELECT MIN(p.id) FROM kaspersky_actual_ip p
WHERE p.addDateTime > SUBDATE(NOW(), INTERVAL %(delete_login_time)s MINUTE))
AND kai1.ipType = 'login')
  AND kai.ipAddress NOT IN (
SELECT DISTINCT kai2.ipAddress
FROM kaspersky_actual_ip kai2
WHERE kai2.active = 1
  AND kai2.ipType IN ('trade', 'static')
  )
  AND kai.active = 1
  AND kai.ipType = 'login'
  AND kai.addDateTime < SUBDATE(NOW(), INTERVAL %(delete_login_time)s MINUTE)
  AND kai.id < (SELECT MIN(p.id) FROM kaspersky_actual_ip p
  WHERE p.addDateTime > SUBDATE(NOW(), INTERVAL %(delete_login_time)s MINUTE))
;'''


delete_login_ip_query = '''DELETE FROM kaspersky_actual_ip
WHERE ipType = 'login'
AND addDateTime < SUBDATE(NOW(), INTERVAL %(delete_login_time)s MINUTE);'''

get_kaspersky_delete_trade_ip_query = '''SELECT
                                     ipOut.ipAddress
                                    FROM (SELECT
                                        kai.id AS id,
                                        kai.ipAddress,
                                        kai1.id AS testLoginId,
                                        kai2.id AS testTradeStaticId
                                      FROM kaspersky_actual_ip kai
                                        LEFT JOIN kaspersky_actual_ip kai1
                                          ON kai1.ipAddress = kai.ipAddress
                                          AND kai1.active = 1
                                          AND kai1.ipType = 'login'
                                          AND kai1.addDateTime >= SUBDATE(NOW(), INTERVAL %(delete_trade_time)s MINUTE)
                                        LEFT JOIN kaspersky_actual_ip kai2
                                          ON kai2.ipAddress = kai.ipAddress
                                          AND kai2.active = 1
                                          AND kai2.ipType IN ('trade', 'static')
                                      WHERE kai.addDateTime < SUBDATE(NOW(), INTERVAL %(delete_trade_time)s MINUTE)
                                      AND kai.active = 1
                                      AND kai.ipType = 'login'
                                      HAVING testLoginId IS NULL AND testTradeStaticId IS NULL
                                    ) AS ipOut
                                    ;'''


delete_trade_ip_query = '''DELETE FROM kaspersky_actual_ip
WHERE ipType = 'trade'
AND addDateTime < SUBDATE(NOW(), INTERVAL %(delete_trade_time)s MINUTE);'''

get_hand_setted_for_delete_query = '''SELECT ipAddress FROM kaspersky_actual_ip WHERE forDelete = 1;'''

delete_hand_setted_for_delete_query = '''DELETE FROM kaspersky_actual_ip
WHERE ipAddress IN (%s);'''

# trade_ip_module
get_trade_ip_query = '''SELECT
          s.remoteAddr
        FROM procedures p
          JOIN procedureRequest r
            ON p.id = r.procedureId
          JOIN organization o
            ON o.id = r.organizationId
          JOIN organizationMember m
            ON r.organizationId = m.organizationId
          JOIN tsdUserActionDayStat s
            ON m.userId = s.userId
        WHERE p.conditionalHoldingDateTime BETWEEN DATE_FORMAT(ADDDATE(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 00:00:00')
        AND DATE_FORMAT(ADDDATE(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 23:59:59')
        AND p.archive = 0
        AND p.actualId IS NULL
        AND p.procedureStatusId IN (4, 22, 65)
        AND r.requestStatusId = 20
        AND (r.customerStatusId IS NULL OR r.customerStatusId = 85)
        AND r.active = 1
        AND r.actualId IS NULL
        AND s.firstActionDateTime > (SELECT
            IFNULL(DATE_FORMAT(MIN(p.publicationDateTime), '%Y-%m-%d %H:%i:%s'), NOW()) AS ch
          FROM procedures p
            JOIN procedureRequest r
              ON p.id = r.procedureId
          WHERE p.conditionalHoldingDateTime BETWEEN DATE_FORMAT(ADDDATE(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 00:00:00')
          AND DATE_FORMAT(ADDDATE(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 23:59:59')
          AND p.procedureStatusId IN (4, 22, 65)
          AND p.archive = 0
          AND p.actualId IS NULL
          AND r.requestStatusId = 20
          AND (r.customerStatusId IS NULL OR r.customerStatusId = 85)
          AND r.active = 1
          AND r.actualId IS NULL)
        GROUP BY s.remoteAddr
        ORDER BY s.remoteAddr
        ;'''







