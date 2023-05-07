from examples.websockets_auth.handlers.models.ping import (
    NotificationMessage,
    NotificationPayload,
    PingPayload,
    PongMessage,
    PongPayload,
)
from fastsockets import handler
from fastsockets.auth.Session import Session
from fastsockets.handlers.auth.SessionExecutor import SessionHandlersExecutor
from fastsockets.handlers.params.Dependency import Depends


def deep_data_provider():
    return 'there'


def additional_data_provider(
    payload: PingPayload,
    session: Session,
    data: str = Depends(deep_data_provider)
) -> str:
    print(f'The session data, the dependency has access to {session.data = }')
    print(f'This is the payload we got in the dependency: {payload = }')
    return f'Hello {data}'



@handler()
async def ping(
    action: str,
    session: Session,
    payload: PingPayload,
    handlers_executor: SessionHandlersExecutor,
    additional_data: str = Depends(additional_data_provider),
) -> PongMessage:
    print(additional_data)
    print(f'Session data, the handler has access to {session.data = }')

    await handlers_executor.broadcast(
        NotificationMessage(
            action='notification',
            payload=NotificationPayload(
                message='A friend requested recieved!',
                level=10
            )
        )
    )

    return PongMessage(
        action='pong',
        payload=PongPayload(
            initiator_action=action,
            message=payload.message,
            success=True
        )
    )
